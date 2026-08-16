# Alp Coder

Alp Coder is a local AI-assisted DevOps agent that translates natural-language requests into controlled Kubernetes, Helm, and Git operations.

## Architecture

```text
Slack / REST API
        |
        v
FastAPI / Slack Bolt
        |
        v
LangChain Agent
        |
        v
Local Ollama LLM
        |
        +--> Kubernetes tools
        +--> Helm tools
        +--> Git tools
```

## Key Features

- Natural-language DevOps requests through Slack
- Local LLM inference with Ollama
- LangChain agent orchestration and tool selection
- Kubernetes CronJob inspection and management
- Helm-based application deployments
- Git-based configuration changes
- FastAPI REST interface
- Environment-level guardrails
- No unrestricted shell access for the LLM

## Demo

### Kubernetes Operations from Slack

Alp Coder can inspect live Kubernetes resources directly through natural-language requests in Slack.

![Slack CronJob Query](docs/images/screenshots)

The result comes from the actual Kubernetes cluster through a controlled tool rather than from the LLM's internal knowledge.

![Kubernetes CronJob Verification](docs/images/screenshots)

### Multi-Tool Git + Helm + Kubernetes Workflow

Alp Coder can also coordinate multiple DevOps tools from a single request.

Example:

```text
@alp coder change nginx hostname in development to alp-coder.local and deploy it
```

![Slack Helm Deployment](docs/images/screenshots)

The agent interprets the request and selects controlled tools that:

1. Update the Helm values
2. Create or reuse a Git branch
3. Commit the configuration change
4. Perform the Helm upgrade
5. Update the application running in Kubernetes

The resulting state can then be independently verified through Helm and Kubernetes.

![Kubernetes Helm Verification](docs/images/screenshots)

## Safety Model

The core design principle behind Alp Coder is:

> **AI interprets intent. Deterministic automation executes infrastructure changes.**

The LLM does not receive unrestricted shell access.

Instead, infrastructure capabilities are exposed through narrowly scoped Python tools. These tools perform the actual Kubernetes, Git, and Helm operations and enforce environment-level guardrails.

Production changes are not executed automatically.

## API

Alp Coder also exposes the agent through a FastAPI REST interface.

```text
POST /api/v1/agent
```

Example request:

```json
{
  "message": "Show me the cronjobs in the test namespace"
}
```

This allows the same underlying agent to be consumed through Slack or programmatically through an API.

## Tech Stack

- Python
- LangChain
- Ollama
- FastAPI
- Slack Bolt / Socket Mode
- Kubernetes
- Minikube
- Helm
- Git

## Local Setup

Create a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the local environment configuration:

```bash
cp .env.example .env
```

Configure your Slack credentials in `.env`:

```text
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Start the Slack bot:

```bash
python -m app.slack_bot
```

## Future Improvements

- Human approval workflows for privileged operations
- PR-based GitOps changes
- Authentication and role-based authorization
- Persistent audit logging
- Agent tracing and evaluation
- Automated testing
- Additional Kubernetes and cloud operations

## Disclaimer

Alp Coder is an independent reference implementation for experimenting with safe AI-assisted infrastructure automation. It is not production infrastructure.