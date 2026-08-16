import subprocess
from pathlib import Path

from langchain.tools import tool


REPO_PATH = Path.home() / "my_ai_project" / "demo-app"
VALUES_FILE = (
    REPO_PATH
    / "environments"
    / "development"
    / "values.yaml"
)


def run_command(command: list[str], cwd: Path) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return f"ERROR: {result.stderr.strip()}"

    return result.stdout.strip()


@tool
def update_nginx_hostname(
    environment: str,
    hostname: str,
) -> str:
    """
    Update the nginx hostname in the development Helm values file,
    create or reuse a Git branch, and commit the change.
    """

    if environment.lower() != "development":
        return "DENIED: only the development environment is allowed."

    if not VALUES_FILE.exists():
        return f"ERROR: Helm values file not found: {VALUES_FILE}"

    branch_name = "update-nginx-hostname"

    original = VALUES_FILE.read_text()

    lines = original.splitlines()

    updated_lines = []
    hostname_found = False

    for line in lines:
        if line.strip().startswith("hostname:"):
            indent = line[: len(line) - len(line.lstrip())]
            updated_lines.append(
                f"{indent}hostname: {hostname}"
            )
            hostname_found = True
        else:
            updated_lines.append(line)

    if not hostname_found:
        return "ERROR: hostname field was not found in values.yaml."

    updated = "\n".join(updated_lines) + "\n"

    if original == updated:
        return (
            f"No change required. nginx hostname is already {hostname}."
        )

    current_branch = run_command(
        ["git", "branch", "--show-current"],
        REPO_PATH,
    )

    if current_branch != branch_name:
        existing_branches = run_command(
            ["git", "branch", "--list", branch_name],
            REPO_PATH,
        )

        if branch_name in existing_branches:
            checkout_result = run_command(
                ["git", "checkout", branch_name],
                REPO_PATH,
            )
        else:
            checkout_result = run_command(
                ["git", "checkout", "-b", branch_name],
                REPO_PATH,
            )

        if checkout_result.startswith("ERROR:"):
            return checkout_result

    VALUES_FILE.write_text(updated)

    add_result = run_command(
        ["git", "add", str(VALUES_FILE)],
        REPO_PATH,
    )

    if add_result.startswith("ERROR:"):
        return add_result

    commit_result = run_command(
        [
            "git",
            "commit",
            "-m",
            f"update nginx hostname to {hostname}",
        ],
        REPO_PATH,
    )

    if commit_result.startswith("ERROR:"):
        return commit_result

    return (
        f"Updated nginx hostname to {hostname} "
        f"in {environment}. "
        f"Git branch: {branch_name}. "
        f"Change committed successfully."
    )