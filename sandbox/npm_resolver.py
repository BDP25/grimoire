import json
from pathlib import Path

import requests
from packaging.version import InvalidVersion
from packaging.version import parse as parse_version


def load_package_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def get_npm_metadata(package_name: str) -> dict | None:
    try:
        r = requests.get(f"https://registry.npmjs.org/{package_name}")
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return None


def extract_repo_url(metadata: dict) -> str | None:
    repo = metadata.get("repository", {})
    url = repo.get("url", "") if isinstance(repo, dict) else repo
    if url.startswith("git+"):
        url = url[4:]
    return url.replace(".git", "").rstrip("/") if "github.com" in url else None


def get_git_tags(owner: str, repo: str) -> list[str]:
    url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    try:
        r = requests.get(url)
        r.raise_for_status()
        return [tag["name"] for tag in r.json()]
    except requests.RequestException:
        return []


def find_tag(tags: list[str], version: str) -> str | None:
    try:
        target = parse_version(version)
        for tag in tags:
            cleaned = tag.lstrip("vV-")
            parsed = parse_version(cleaned)
            if parsed == target:
                return tag
    except InvalidVersion:
        pass
    return None


def process_package_json(path: Path) -> None:
    data = load_package_json(path)
    deps = data.get("dependencies", {})
    print("\n🔍 Matched JS Dependencies:\n")

    for name, version in deps.items():
        metadata = get_npm_metadata(name)
        if not metadata:
            print(f"Could not fetch metadata for {name}")
            continue

        repo_url = extract_repo_url(metadata)
        if not repo_url:
            print(f"No GitHub repo found for {name}")
            continue

        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            print(f"Invalid GitHub URL: {repo_url}")
            continue
        owner, repo = parts[-2], parts[-1]

        tags = get_git_tags(owner, repo)
        matched = find_tag(tags, version)

        print(
            f"Name: {name}\nVersion: {version}\nRepo: {repo_url}\nTag: {matched or 'N/A'}\n"
        )


if __name__ == "__main__":
    process_package_json(Path("package.json"))
