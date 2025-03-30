from pathlib import Path
from tempfile import TemporaryDirectory

from repo_clone import clone_and_process

# List of repositories to clone
REPOS = ["https://github.com/psf/requests.git"]

# Store results here
cloned_repo_titles: list = []

if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"Cloning into temporary directory: {temp_path}\n")

        for repo in REPOS:
            clone_and_process(repo, temp_path)

        print("\nResults:")
        for repo_url, title in cloned_repo_titles:
            print(f"{repo_url} -> {title}")
