import re
from pathlib import Path

import requests
import toml
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import InvalidVersion, Version
from packaging.version import parse as parse_version


def get_pyproject_dependencies(pyproject_path: Path) -> dict:
    data = toml.load(pyproject_path)
    deps = data.get("project", {}).get("dependencies", {})
    if not deps:
        deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})

    parsed = {}

    if isinstance(deps, list):
        for entry in deps:
            try:
                req = Requirement(entry)
                parsed[req.name] = str(req.specifier) or "*"
            except Exception as e:
                print(f"Could not parse dependency: {entry} ({e})")

    elif isinstance(deps, dict):
        for name, version_spec in deps.items():
            if isinstance(version_spec, str):
                try:
                    req = Requirement(f"{name} {version_spec}")
                    parsed[req.name] = str(req.specifier) or "*"
                except Exception as e:
                    print(f"Could not parse dependency: {name} {version_spec} ({e})")
            elif isinstance(version_spec, dict):
                parsed[name] = version_spec.get("version", "*")
    return parsed


def get_pypi_metadata(package_name: str) -> dict | None:
    try:
        r = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        r.raise_for_status()
        return r.json()
    except requests.HTTPError:
        return None


def extract_repo_url(package_name: str, metadata: dict) -> str | None:
    if package_name.startswith("types-"):
        return "https://github.com/python/typeshed"
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


VERSION_TAG_PATTERN = re.compile(r"^v?(\d+\.\d+\.\d+)$")


def find_best_matching_tag(
    tags: list[str], specifier: SpecifierSet
) -> tuple[str, Version] | None:
    matching_versions = []
    for tag in tags:
        match = VERSION_TAG_PATTERN.match(tag)
        if not match:
            continue

        version_str = match.group(1)  # Extract the version part, e.g. "1.2.3"
        try:
            parsed = parse_version(version_str)
            if isinstance(parsed, Version) and parsed in specifier:
                matching_versions.append((parsed, tag))
        except InvalidVersion:
            continue

    if matching_versions:
        best = max(matching_versions, key=lambda x: x[0])
        return best[1], best[0]
    return None


def clean_dep_name(dep: str) -> str:
    return dep.split("[")[0].strip()


def process(pyproject_path: Path) -> None:
    deps = get_pyproject_dependencies(pyproject_path)
    print("\n🔍 Matched Dependencies:\n")
    if not deps:
        print("No dependencies found.")
        return

    for dep, version_spec in deps.items():
        base_name = clean_dep_name(dep)

        try:
            spec = SpecifierSet(version_spec)
        except Exception:
            print(f"Skipping {base_name}: Invalid version specifier '{version_spec}'")
            continue

        metadata = get_pypi_metadata(base_name)
        if not metadata:
            print(f"Could not fetch metadata for {base_name}")
            continue

        if not has_classifiers(metadata):
            print(f"Skipping {base_name}: No classifiers")
            continue

        repo_url = extract_repo_url(base_name, metadata)
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
            print(
                f"Name: {base_name}\nVersion: {version_spec}\nRepo: {repo_url}\nTag: N/A (no tags found)\n"
            )
            continue

        matched = find_best_matching_tag(tags, spec)
        if not matched:
            print(f"No matching tag for {base_name} ({version_spec})")
            continue

        matched_tag, matched_version = matched
        print(
            f"Name: {base_name}\nVersion: {version_spec}\nRepo: {repo_url}\nTag: {matched_tag}\n"
        )


if __name__ == "__main__":
    process(Path(__file__).parent / "pyproject_test.toml")
