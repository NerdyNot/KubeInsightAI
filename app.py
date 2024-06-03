import os
import yaml
import smtplib
import argparse
import requests
import markdown2
from kubernetes import client, config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from openai import OpenAI, AzureOpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# OpenAI client setup function
def set_openai_client(openai_config):
    client_type = openai_config['type'].strip().lower()
    api_key = openai_config['api_key'].strip()
    model = openai_config['model'].strip()
    
    if client_type == "azure":
        azure_endpoint = openai_config['azure_endpoint'].strip()
        azure_apiversion = openai_config['azure_apiversion'].strip()
        return AzureOpenAI(
            api_version=azure_apiversion,
            azure_endpoint=azure_endpoint
        ), client_type, model
    else:
        return OpenAI(api_key=api_key), client_type, model

# Function to collect and filter Kubernetes information
def collect_k8s_info(kubeconfig_path, context):
    config.load_kube_config(config_file=kubeconfig_path, context=context)
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    metrics_v1 = client.CustomObjectsApi()
    
    # Collecting Nodes information
    nodes_info = []
    nodes = v1.list_node().items
    for node in nodes:
        nodes_info.append({
            "name": node.metadata.name,
            "status": node.status.conditions[-1].status,
            "role": node.metadata.labels.get('kubernetes.io/role', 'N/A')
        })
    
    # Collecting Pods information
    pods_info = []
    pods = v1.list_pod_for_all_namespaces().items
    for pod in pods:
        pods_info.append({
            "namespace": pod.metadata.namespace,
            "name": pod.metadata.name,
            "status": pod.status.phase
        })
    
    # Collecting Services information
    services_info = []
    services = v1.list_service_for_all_namespaces().items
    for svc in services:
        services_info.append({
            "namespace": svc.metadata.namespace,
            "name": svc.metadata.name,
            "type": svc.spec.type,
            "cluster_ip": svc.spec.cluster_ip
        })
    
    # Collecting Deployments information
    deployments_info = []
    deployments = apps_v1.list_deployment_for_all_namespaces().items
    for deploy in deployments:
        deployments_info.append({
            "namespace": deploy.metadata.namespace,
            "name": deploy.metadata.name,
            "replicas": deploy.spec.replicas
        })
    
    # Collecting PersistentVolumeClaims information
    pvcs_info = []
    pvcs = v1.list_persistent_volume_claim_for_all_namespaces().items
    for pvc in pvcs:
        pvcs_info.append({
            "namespace": pvc.metadata.namespace,
            "name": pvc.metadata.name,
            "status": pvc.status.phase
        })

    # Collecting Secrets information
    secrets_info = []
    secrets = v1.list_secret_for_all_namespaces().items
    for secret in secrets:
        secrets_info.append({
            "namespace": secret.metadata.namespace,
            "name": secret.metadata.name,
            "type": secret.type
        })
    
    # Collecting Events information
    events_info = []
    events = v1.list_event_for_all_namespaces().items
    for event in events:
        events_info.append({
            "namespace": event.metadata.namespace,
            "name": event.metadata.name,
            "message": event.message,
            "type": event.type,
            "reason": event.reason,
            "timestamp": event.last_timestamp
        })

    # Collecting Resource Usage
    nodes_usage = metrics_v1.list_cluster_custom_object(group="metrics.k8s.io", version="v1beta1", plural="nodes")
    pods_usage = metrics_v1.list_cluster_custom_object(group="metrics.k8s.io", version="v1beta1", plural="pods")

    # Calculating counts for the overview section
    overview_info = {
        "node_agents": len([node for node in nodes_info if 'agent' in node['role']]),
        "node_users": len([node for node in nodes_info if 'user' in node['role']]),
        "namespaces": len(set(pod['namespace'] for pod in pods_info)),
        "services": len(services_info),
        "deployments": len(deployments_info),
        "statefulsets": len([deploy for deploy in deployments_info if 'statefulset' in deploy['name'].lower()]),
        "replicasets": len([deploy for deploy in deployments_info if 'replicaset' in deploy['name'].lower()]),
        "pods": len(pods_info),
        "pvcs": len(pvcs_info),
        "secrets": len(secrets_info)
    }

    return {
        "nodes": nodes_info,
        "pods": pods_info,
        "services": services_info,
        "deployments": deployments_info,
        "pvcs": pvcs_info,
        "secrets": secrets_info,
        "events": events_info,
        "nodes_usage": nodes_usage,
        "pods_usage": pods_usage,
        "overview": overview_info
    }

# Function to generate report using OpenAI
def generate_report(client, model, k8s_info, language):
    system_prompt = f"""
    # Instruction
     - You are an assistant specialized in Kubernetes. Using the provided Kubernetes cluster information, generate a comprehensive status report. 
     - You must generate the report in {language}
     - Your responses should be informative, visually appealing, logical and actionable.
    
    # Report Example:
    # Kubernetes Cluster Status Report

    ## Node Status:
    - For each node, include:
        - Name
        - Role
        - Status
        - Resource Usage (CPU in m, Memory in Gi)
    
    ## OverView:
    - Nodes(Agent/Users) : {k8s_info['overview']['node_agents']}/{k8s_info['overview']['node_users']} ea
    - Namespaces : {k8s_info['overview']['namespaces']} ea
    - Services : {k8s_info['overview']['services']} ea
    - Deployments : {k8s_info['overview']['deployments']} ea
    - StatefulSets : {k8s_info['overview']['statefulsets']} ea
    - ReplicaSets : {k8s_info['overview']['replicasets']} ea
    - Pods : {k8s_info['overview']['pods']} ea
    - PersistentVolumeClaims : {k8s_info['overview']['pvcs']} ea
    - Secrets : {k8s_info['overview']['secrets']} ea

        
    ## Pod Status:
    - Include the overall pod status across all nodes (e.g., all pods are running)
    - Highlight key pods, including their namespace, name, status, and resource usage (CPU in m, Memory in Gi)

    ## Deployment Status:
    - For each namespace, list all deployments, including the name and replica count

    ## Service Status:
    - For each namespace, list all services, including the name, type, and cluster IP

    ## Events:
    - List any significant events, including their namespace, name, message, type, reason, and timestamp

    ## Potential Issues and Recommendations:
    - Identify any pods with high CPU or memory usage and recommend adjustments
    - Suggest scaling strategies if necessary
    - Recommend setting up monitoring tools
    - Provide suggestions for namespace and node pool management
    """

    user_input = f"Kubernetes Info: {yaml.dump(k8s_info)}"

    console = Console()
    with console.status("[bold green]Generating Kubernetes report...[/bold green]"):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_input}
            ],
            temperature=1,
            max_tokens=4095,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

    report = response.choices[0].message.content.strip()
    return report

# Function to send report via email
def send_email(report, email_config):
    msg = MIMEMultipart()
    msg['From'] = email_config['from_email']
    msg['To'] = email_config['to_email']
    msg['Subject'] = email_config['subject']
    html_report = markdown2.markdown(report)
    msg.attach(MIMEText(html_report, 'html'))

    server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
    server.starttls()
    server.login(email_config['from_email'], email_config['password'])
    server.send_message(msg)
    server.quit()

# Function to send report via Slack webhook
def send_slack_message(report, slack_config):
    payload = {
        "text": "Kubernetes Cluster Status Report",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": report
                }
            }
        ]
    }
    response = requests.post(slack_config['webhook_url'], json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

# Function to save report to file
def save_to_file(report, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(report)

# Function to load configuration
def load_configuration(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    return config_data

# Main function
def main():
    parser = argparse.ArgumentParser(description="Kubernetes Report Generator")
    parser.add_argument("-c", "--config-file", required=True, help="Path to the configuration YAML file")
    parser.add_argument("-m", "--mode", required=True, choices=['email', 'slack', 'output', 'file'], help="Mode of report delivery: email, slack, output, file")
    parser.add_argument("-f", "--file", help="Path to save the report if mode is 'file'")
    parser.add_argument("-C","--context", required=True, help="Kubernetes context to use")
    parser.add_argument("-L","--language", required=True, help="Language for the report (e.g., English, Korean)")
    args = parser.parse_args()

    # Load configuration
    config_data = load_configuration(config_file=args.config_file)

    openai_config = config_data['openai']
    kubernetes_config = config_data['kubernetes']
    email_config = config_data.get('email', {})
    slack_config = config_data.get('slack', {})

    # Set up the OpenAI client
    client, client_type, model = set_openai_client(openai_config)

    # Collect Kubernetes information
    k8s_info = collect_k8s_info(kubernetes_config['kubeconfig'], args.context)

    # Generate report
    report = generate_report(client, model, k8s_info, args.language)

    console = Console()
    md = Markdown(report)
    
    if args.mode == 'output':
        console.print(Panel(md, title="[bold yellow]Kubernetes Status Report[/bold yellow]"))
    elif args.mode == 'email':
        send_email(report, email_config)
    elif args.mode == 'slack':
        send_slack_message(report, slack_config)
    elif args.mode == 'file':
        if args.file:
            save_to_file(report, args.file)
        else:
            console.print("[bold red]File path must be provided when mode is 'file'[/bold red]")

if __name__ == "__main__":
    main()
