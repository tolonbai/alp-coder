import subprocess
from pathlib import Path

from langchain.tools import tool


REPO_PATH = Path.home() / "my_ai_project" / "demo-app"


def run_command(command: list[str]) -> str:
    result = subprocess.run(
        command,
        cwd=REPO_PATH,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return f"ERROR: {result.stderr.strip()}"

    return result.stdout.strip()


@tool
def deploy_nginx_helm(environment: str) -> str:
    """
    Deploy or upgrade the nginx-demo Helm release
    using the requested environment values.
    """

    if environment.lower() != "development":
        return "DENIED: only development deployment is allowed."

    values_file = f"environments/{environment}/values.yaml"

    result = run_command([
        "helm",
        "upgrade",
        "--install",
        "nginx-demo",
        ".",
        "-f",
        values_file,
        "-n",
        environment,
    ])

    if result.startswith("ERROR:"):
        return result

    return (
        f"Helm deployment succeeded for nginx-demo "
        f"in {environment}.\n\n{result}"
    )