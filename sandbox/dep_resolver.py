import shutil
import tempfile
from pathlib import Path

import requests
import toml
from git import Repo
from packaging.version import InvalidVersion
from packaging.version import parse as parse_version


def get_pyproject_dependencies(pyproject_path: Path) -> dict:
    data = toml.load(pyproject_path)
    deps = data.get("project", {}).get("dependencies", {})
    if not deps:
        deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})

    # Handle both dict- and list-style dependencies
    if isinstance(deps, list):
        parsed = {}
        for entry in deps:
            if "==" in entry:
                name, version = entry.split("==", 1)
                parsed[name.strip()] = f"=={version.strip()}"
            else:
                parsed[entry.strip()] = "*"
        return parsed
    return deps


def get_pypi_metadata(package_name: str) -> dict | None:
    try:
        r = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        r.raise_for_status()
        return r.json()
    except requests.HTTPError:
        return None


def extract_repo_url(metadata: dict) -> str | None:
    urls = metadata["info"].get("project_urls", {})
    for key in ["Source", "Repository", "Homepage"]:
        url = urls.get(key, "")
        if "github.com" in url:
            return url.rstrip("/")
    homepage = metadata["info"].get("home_page", "")
    return homepage if "github.com" in homepage else None


def has_classifiers(metadata: dict) -> bool:
    return bool(metadata["info"].get("classifiers"))


def get_git_tags(owner: str, repo: str) -> list[str]:
    url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    try:
        r = requests.get(url)
        r.raise_for_status()
        return [tag["name"] for tag in r.json()]
    except Exception:
        return []


def find_matching_tag(tags: list[str], version: str) -> str | None:
    parsed_target = parse_version(version)
    for tag in tags:
        try:
            parsed_tag = parse_version(tag.lstrip("v"))
            if parsed_tag == parsed_target:
                return tag
        except InvalidVersion:
            continue
    return None


def clone_and_checkout(repo_url: str, tag: str) -> None:
    temp_dir = tempfile.mkdtemp()
    try:
        repo = Repo.clone_from(repo_url, temp_dir)
        repo.git.checkout(tag)
        print(f"Cloned {repo_url} at tag {tag}")
    except Exception as e:
        print(f"Failed to clone {repo_url} at tag {tag}: {e}")
    finally:
        shutil.rmtree(temp_dir)


def clean_dep_name(dep: str) -> str:
    return dep.split("[")[0].strip()


def process(pyproject_path: Path) -> None:
    deps = get_pyproject_dependencies(pyproject_path)
    print(f"Loaded dependencies: {deps}")  # Debug print
    if not deps:
        print("No dependencies found.")
        return

    any_processed = False
    for dep, version_spec in deps.items():
        if "==" not in version_spec:
            continue

        version = version_spec.split("==")[1].strip()
        base_name = clean_dep_name(dep)

        print(f"Processing {base_name}=={version}...")
        metadata = get_pypi_metadata(base_name)
        if not metadata:
            print(f"Could not fetch metadata for {base_name}")
            continue

        if not has_classifiers(metadata):
            print(f"Skipping {base_name}: No classifiers")
            continue

        repo_url = extract_repo_url(metadata)
        if not repo_url or "github.com" not in repo_url:
            print(f"No GitHub repo found for {base_name}")
            continue

        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            print(f"Invalid GitHub URL: {repo_url}")
            continue
        owner, repo = parts[-2], parts[-1]

        tags = get_git_tags(owner, repo)
        if not tags:
            print(f"No tags found for {base_name}")
            continue

        tag = find_matching_tag(tags, version)
        if not tag:
            print(f"No matching tag for version {version}")
            continue

        clone_and_checkout(repo_url, tag)
        any_processed = True

    if not any_processed:
        print("Done. No dependencies matched the processing criteria.")


if __name__ == "__main__":
    process(Path("..") / "pyproject.toml")
