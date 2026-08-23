import subprocess
from datetime import datetime
from pathlib import Path


def run_git_command(
    arguments,
    check=True
):
    result = subprocess.run(
        ["git"] + arguments,
        capture_output=True,
        text=True
    )

    if check and result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
            or result.stdout.strip()
            or "Git command failed."
        )

    return result


def is_git_repository():

    result = run_git_command(
        [
            "rev-parse",
            "--is-inside-work-tree"
        ],
        check=False
    )

    return (
        result.returncode == 0
        and result.stdout.strip() == "true"
    )


def has_remote_origin():

    result = run_git_command(
        [
            "remote",
            "get-url",
            "origin"
        ],
        check=False
    )

    return result.returncode == 0


def get_current_branch():

    result = run_git_command(
        [
            "branch",
            "--show-current"
        ]
    )

    branch = result.stdout.strip()

    if not branch:
        return "main"

    return branch


def has_changes():

    result = run_git_command(
        [
            "status",
            "--porcelain"
        ]
    )

    return bool(
        result.stdout.strip()
    )


def publish_to_github(
    project_name=None,
    commit_message=None
):

    print(
        "\nPreparing GitHub publication..."
    )

    if not is_git_repository():
        raise RuntimeError(
            "This folder is not yet a Git repository."
        )

    if not has_remote_origin():
        raise RuntimeError(
            "No GitHub remote named 'origin' "
            "is connected yet."
        )

    if not has_changes():

        print(
            "No new changes to publish."
        )

        return False

    run_git_command(
        [
            "add",
            "."
        ]
    )

    if commit_message is None:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        if project_name:
            commit_message = (
                f"Update {project_name} "
                f"competitive intelligence "
                f"{timestamp}"
            )
        else:
            commit_message = (
                f"Update competitive intelligence "
                f"{timestamp}"
            )

    print(
        f"Commit message: "
        f"{commit_message}"
    )

    run_git_command(
        [
            "commit",
            "-m",
            commit_message
        ]
    )

    branch = get_current_branch()

    print(
        f"Pushing branch: {branch}"
    )

    run_git_command(
        [
            "push",
            "origin",
            branch
        ]
    )

    print(
        "\nGitHub successfully updated."
    )

    return True