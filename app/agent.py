from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from app.tools.helm import deploy_nginx_helm

from app.tools.kubernetes import (
    list_cronjobs,
    suspend_cronjob,
)

from app.tools.gitops import (
    update_nginx_hostname,
)


# Local LLM running through Ollama
model = ChatOllama(
    model="qwen3:4b",
    temperature=0,
)


# Tools Alp Coder is allowed to use
tools = [
    list_cronjobs,
    suspend_cronjob,
    update_nginx_hostname,
    deploy_nginx_helm,
]


# Create the LangChain agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
You are Alp Coder, an AI DevOps assistant.

You help engineers operate infrastructure safely using only
the tools that have been explicitly provided to you.

Rules:

1. Use only the provided tools for infrastructure operations.
2. Never invent infrastructure state.
3. Never invent or execute arbitrary shell commands.
4. Read-only Kubernetes operations are allowed.
5. Non-production modifications may be performed using approved tools.
6. Production modifications require human approval.
7. Prefer Git-based configuration changes when modifying application configuration.
8. If no appropriate tool exists, clearly explain that the requested operation cannot be performed.
9. Clearly summarize what action was performed and whether it succeeded.
""",
)