# KubeInsightAI

KubeInsightAI is a tool that analyzes the status of Kubernetes clusters, generates reports, and delivers them via email, Slack, or saves them as files. The tool leverages OpenAI or Azure OpenAI to generate the reports. It uses the Kubernetes API to gather cluster status information and automatically generates a report to help administrators easily understand the state of the cluster.

## Features

- Collects Kubernetes cluster status information
- Generates reports using OpenAI or Azure OpenAI
- Delivers reports via email, Slack, or saves them as files
- Provides various configuration options

## Prerequisites

- Python 3.8+
- OpenAI or Azure OpenAI API key
- Access to Kubernetes cluster (kubeconfig file)
- rich (for terminal output formatting)
- PyYAML (for parsing YAML configuration files)
- markdown2 (for converting Markdown to HTML)
- requests (for sending Slack webhooks)

## Installation

1. Clone the repository.

```sh
git clone https://github.com/NerdyNot/KubeInsightAI.git
cd KubeInsightAI
```

2. Create and activate a virtual environment.

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required packages.

```sh
pip install -r requirements.txt
```

## Configuration

Create a `config.yaml` file in the project directory with the following structure.

```yaml
openai:
  type: "openai"  # Specify "openai" or "azure". If "azure" is chosen, you must set azure_endpoint and azure_apiversion below.
  api_key: "your_openai_or_azure_api_key"  # Enter your OpenAI or Azure OpenAI API key.
  model: "your_openai_model_id"  # Enter the model ID you want to use, e.g., "gpt-4" or another model ID.
  azure_endpoint: "your_azure_openai_endpoint"  # Set this only if type is "azure". Example: "https://your-resource-name.openai.azure.com/"
  azure_apiversion: "your_azure_api_version"  # Set this only if type is "azure". Example: "2023-05-15"

kubernetes:
  kubeconfig: "/path/to/your/kubeconfig"  # Path to your kubeconfig file.

email:
  from_email: "your_email@example.com"
  to_email: "recipient_email@example.com"
  subject: "Kubernetes Cluster Status Report"
  smtp_server: "smtp.example.com"
  smtp_port: 587
  password: "your_email_password"

slack:
  webhook_url: "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
```

## Usage

To generate a status report for your Kubernetes cluster, run the script with the appropriate arguments.

```sh
python app.py -c config.yaml --context your_kube_context -L korean -m output
```

### Command-line Arguments

- `-c`, `--config-file`: Path to the configuration YAML file (required).
- `-m`, `--mode`: Mode of report delivery: `email`, `slack`, `output`, `file` (required).
- `-f`, `--file`: Path to save the report if mode is `file` (optional).
- `-C`, `--context`: Kubernetes context to use (required).
- `-L`, `--language`: Language for the report (e.g., English, Korean) (required).

### Example

To save the report to a file:

```sh
python app.py -c config.yaml --context your_kube_context -L korean -m file -f "/path/to/report.txt"
```

To send the report to Slack:

```sh
python app.py -c config.yaml --context your_kube_context -L english -m slack
```

### Important Notices

1. **Using the `--mode` Option**
   - The `--mode` option allows you to deliver the report via email, Slack, output to console, or save to a file.

2. **Appropriate Configuration**
   - Ensure the appropriate configurations (e.g., email settings, Slack webhook URL) are accurately specified in the `config.yaml` file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Libraries and Licenses

### OpenAI
[OpenAI](https://www.openai.com/)
[Azure OpenAI](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/)
- **Description**: Official OpenAI Python client library, providing convenient access to the OpenAI API.
- **License**: Apache License 2.0
- **Usage**: Used to interact with the OpenAI API for generating reports based on Kubernetes data.

### Kubernetes
[Kubernetes Python Client](https://github.com/kubernetes-client/python)
- **Description**: Official Python client library for Kubernetes.
- **License**: Apache License 2.0
- **Usage**: Used to interact with the Kubernetes API to collect cluster data.

### Rich
[Rich](https://github.com/Textualize/rich)
- **Description**: Python library for rich text and beautiful formatting in the terminal.
- **License**: MIT
- **Usage**: Used for formatting console output.

### PyYAML
[PyYAML](https://pyyaml.org/)
- **Description**: Python library for YAML parsing and emitting.
- **License**: MIT
- **Usage**: Used for parsing the YAML configuration file.

### markdown2
[markdown2](https://github.com/trentm/python-markdown2)
- **Description**: A fast and complete implementation of Markdown in Python.
- **License**: MIT
- **Usage**: Used to convert Markdown to HTML for email reports.

### Requests
[Requests](https://docs.python-requests.org/en/latest/)
- **Description**: A simple, yet elegant HTTP library for Python.
- **License**: Apache License 2.0
- **Usage**: Used to send HTTP requests to Slack webhook URLs.

# KubeInsightAI

KubeInsightAI는 Kubernetes 클러스터의 상태를 분석하고 보고서를 생성하여 이메일이나 Slack으로 전송하거나 파일로 저장하는 도구입니다. 이 도구는 OpenAI 또는 Azure OpenAI를 활용하여 보고서를 생성합니다. Kubernetes API를 사용하여 클러스터의 상태를 수집하고, 보고서를 자동으로 생성하여 관리자가 클러스터의 상태를 쉽게 파악할 수 있도록 도와줍니다.

## 기능

- Kubernetes 클러스터 상태 정보 수집
- OpenAI 또는 Azure OpenAI를 사용하여 보고서 생성
- 보고서를 이메일, Slack 또는 파일로 저장 가능
- 다양한 구성 옵션 제공

## 사전 요구 사항

- Python 3.8+
- OpenAI 또는 Azure OpenAI API 키
- Kubernetes 클러스터에 대한 접근 권한 (kubeconfig 파일)
- rich (터미널 출력 포맷팅용)
- PyYAML (YAML 구성 파일 파싱용)
- markdown2 (Markdown을 HTML로 변환)
- requests (Slack 웹훅 전송용)

## 설치

1. 리포지토리를 복제합니다.

```sh
git clone https://github.com/NerdyNot/KubeInsightAI.git
cd KubeInsightAI
```

2. 가상 환경을 만들고 활성화합니다.

```sh
python -m venv venv
source venv/bin/activate  # Windows의 경우 `venv\Scripts\activate` 사용
```

3. 필요한 패키지를 설치합니다.

```sh
pip install -r requirements.txt
```

## 구성

프로젝트 디렉터리에 `config.yaml` 파일을 아래와 같은 구조로 생성합니다.

```yaml
openai:
  type: "openai"  # "openai" 또는 "azure" 지정. "azure"가 선택되면 아래에 azure_endpoint와 azure_apiversion을 설정해야 합니다.
  api_key: "your_openai_or_azure_api_key"  # OpenAI 또는 Azure OpenAI API 키를 입력합니다.
  model: "your_openai_model_id"  # 사용하고자 하는 모델 ID를 입력합니다. 예: "gpt-4" 또는 다른 모델 ID.
  azure_endpoint: "your_azure_openai_endpoint"  # type이 "azure"인 경우에만 설정합니다. 예: "https://your-resource-name.openai.azure.com/"
  azure_apiversion: "your_azure_api_version"  # type이 "azure"인 경우에만 설정합니다. 예: "2023-05-15"

kubernetes:
  kubeconfig: "/path/to/your/kubeconfig"  # kubeconfig 파일의 경로를 입력합니다.

email:
  from_email: "your_email@example.com"
  to_email: "recipient_email@example.com"
  subject: "Kubernetes Cluster Status Report"
  smtp_server: "smtp.example.com"
  smtp_port: 587
  password: "your_email_password"

slack:
  webhook_url: "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
```

## 사용법

Kubernetes 클러스터의 상태 보고서를 생성하려면 적절한 인자와 함께 스크립트를 실행합니다.

```

sh
python app.py -c config.yaml --context your_kube_context -L korean -m output
```

### 명령줄 인수

- `-c`, `--config-file`: 구성 YAML 파일의 경로 (필수).
- `-m`, `--mode`: 보고서 전달 방식: `email`, `slack`, `output`, `file` 중 하나를 선택 (필수).
- `-f`, `--file`: 파일로 저장할 경우 파일 경로 (선택적).
- `-C`, `--context`: 사용할 Kubernetes 컨텍스트 (필수).
- `-L`, `--language`: 보고서의 언어 (예: English, Korean) (필수).

### 예시

보고서를 파일로 저장하는 예시:

```sh
python app.py -c config.yaml --context your_kube_context -L korean -m file -f "/path/to/report.txt"
```

Slack으로 보고서를 전송하는 예시:

```sh
python app.py -c config.yaml --context your_kube_context -L english -m slack
```

### 중요 사항

1. **`--mode` 옵션 사용**
   - `--mode` 옵션을 사용하여 보고서를 이메일, Slack, 출력 또는 파일로 저장할 수 있습니다.

2. **적절한 구성**
   - 각 모드에 필요한 구성 (예: 이메일 설정, Slack 웹훅 URL)을 `config.yaml` 파일에 정확히 입력해야 합니다.

## 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하십시오.

## 기여

개선 사항이나 버그 수정을 위한 이슈를 열거나 풀 리퀘스트를 제출해 주세요.

## 라이브러리 및 라이센스

### OpenAI
[OpenAI](https://www.openai.com/)
[Azure OpenAI](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/)
- **설명**: 공식 OpenAI Python 클라이언트 라이브러리로, OpenAI API에 편리하게 접근할 수 있습니다.
- **라이센스**: Apache License 2.0
- **사용 용도**: Kubernetes 데이터를 기반으로 보고서를 생성하기 위해 OpenAI API와 상호 작용하는 데 사용됩니다.

### Kubernetes
[Kubernetes Python Client](https://github.com/kubernetes-client/python)
- **설명**: 공식 Python 클라이언트 라이브러리로, Kubernetes와 상호 작용할 수 있습니다.
- **라이센스**: Apache License 2.0
- **사용 용도**: Kubernetes API와 상호 작용하여 클러스터 데이터를 수집하는 데 사용됩니다.

### Rich
[Rich](https://github.com/Textualize/rich)
- **설명**: 터미널에서 리치 텍스트 및 아름다운 포맷을 제공하는 Python 라이브러리입니다.
- **라이센스**: MIT
- **사용 용도**: 콘솔 출력을 포맷하는 데 사용됩니다.

### PyYAML
[PyYAML](https://pyyaml.org/)
- **설명**: YAML 파싱 및 방출을 위한 Python 라이브러리입니다.
- **라이센스**: MIT
- **사용 용도**: YAML 구성 파일을 파싱하는 데 사용됩니다.

### markdown2
[markdown2](https://github.com/trentm/python-markdown2)
- **설명**: Python에서 Markdown을 빠르고 완전하게 구현한 라이브러리입니다.
- **라이센스**: MIT
- **사용 용도**: 이메일 보고서를 위해 Markdown을 HTML로 변환하는 데 사용됩니다.

### Requests
[Requests](https://docs.python-requests.org/en/latest/)
- **설명**: Python을 위한 간단하고 우아한 HTTP 라이브러리입니다.
- **라이센스**: Apache License 2.0
- **사용 용도**: Slack 웹훅 URL로 HTTP 요청을 보내는 데 사용됩니다.