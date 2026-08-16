import subprocess
from langchain.tools import tool


def run_command(command: list[str]) -> str:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return f"ERROR: {result.stderr.strip()}"

    return result.stdout.strip()


@tool
def list_cronjobs(namespace: str) -> str:
    """List Kubernetes CronJobs in the requested namespace."""

    return run_command([
        "kubectl",
        "get",
        "cronjobs",
        "-n",
        namespace,
        "-o",
        "wide",
    ])


@tool
def suspend_cronjob(namespace: str, name: str) -> str:
    """Suspend a Kubernetes CronJob in a non-production namespace."""

    if namespace.lower() in {"prod", "production"}:
        return "DENIED: Production modifications require human approval."

    return run_command([
        "kubectl",
        "patch",
        "cronjob",
        name,
        "-n",
        namespace,
        "-p",
        '{"spec":{"suspend":true}}',
    ])