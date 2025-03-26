from pathlib import Path
from tempfile import TemporaryDirectory

from git import Repo
from git.exc import GitCommandError

# List of repositories to clone
REPOS = [
    "https://github.com/psf/requests.git",
    "https://github.com/pallets/flask.git",
    "https://github.com/tiangolo/fastapi.git",
    "https://github.com/encode/httpx.git",
    "https://github.com/streamlit/streamlit.git",
]

# Store results here
cloned_repo_titles = []


def extract_readme_title(repo_path: Path) -> str:
    readme = repo_path / "README.md"
    if readme.exists():
        with readme.open("r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):
                    return line.strip("# \n")
    return "No title found"


def clone_and_process(repo_url: str, base_path: Path) -> None:
    repo_name = repo_url.rstrip(".git").split("/")[-1]
    target_path = base_path / repo_name
    try:
        Repo.clone_from(repo_url, to_path=target_path, depth=1)
        title = extract_readme_title(target_path)
        cloned_repo_titles.append((repo_url, title))
    except GitCommandError as e:
        print(f"Failed to clone {repo_url}: {e}")
        cloned_repo_titles.append((repo_url, "Clone failed"))


if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"Cloning into temporary directory: {temp_path}\n")

        for repo in REPOS:
            clone_and_process(repo, temp_path)

        print("\nResults:")
        for repo_url, title in cloned_repo_titles:
            print(f"{repo_url} -> {title}")
