import subprocess


def get_git_commit_hash() -> str:
    try:
        commit_hash = (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .decode("utf-8")
            .strip()
        )
        return commit_hash
    except subprocess.CalledProcessError:
        return "Not a git repository or no commits found"
