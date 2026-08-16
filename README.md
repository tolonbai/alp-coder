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

Key Features
Natural-language DevOps requests through Slack
Local LLM inference with Ollama
LangChain tool selection
Kubernetes CronJob inspection and management
Helm-based application deployment
Git-based configuration changes
FastAPI REST endpoint
Environment-level guardrails
No unrestricted shell access for the LLM
Example Workflow

User:

@alp coder change nginx hostname in development to alp-coder.local and deploy it

Alp Coder:

Updates Helm values
Creates or reuses a Git branch
Commits the configuration change
Performs a Helm upgrade
Updates the workload in Kubernetes
Safety Model

The LLM interprets intent and selects tools.

Deterministic Python functions perform infrastructure operations and enforce guardrails.

Production changes are not executed automatically.

Tech Stack
Python
LangChain
Ollama
FastAPI
Slack Bolt / Socket Mode
Kubernetes
Minikube
Helm
Git
Local Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Create a local environment file:

cp .env.example .env

Then configure your Slack tokens in .env.

Disclaimer

This is an independent reference implementation for experimenting with safe AI-assisted infrastructure automation. It is not production infrastructure.