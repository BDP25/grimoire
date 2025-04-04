from pathlib import Path

import requests
import toml


def get_pyproject_dependencies(pyproject_path: Path) -> dict:
    data = toml.load(pyproject_path)
    deps = data.get("project", {}).get("dependencies", {})
    if not deps:
        deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    return deps


def get_pypi_repo_url(package_name: str, version: str | None = None) -> str:
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        repo_url = None
        project_urls = data["info"].get("project_urls", {})
        for key in ["Source", "Homepage", "Repository"]:
            if key in project_urls:
                repo_url = project_urls[key]
                break
        if not repo_url:
            repo_url = data["info"].get("home_page", "No repository URL found")
        if version and repo_url and "github.com" in repo_url:
            tag_candidates = [f"v{version}", version]
            parts = repo_url.rstrip("/").split("/")
            if len(parts) >= 5:
                owner, repo = parts[-2], parts[-1]
                api_url = f"https://api.github.com/repos/{owner}/{repo}/tags"
                tags_response = requests.get(api_url)
                if tags_response.status_code == 200:
                    tags = tags_response.json()
                    for tag in tags:
                        if tag.get("name") in tag_candidates:
                            repo_url = f"{repo_url}/tree/{tag.get('name')}"
                            break
        return repo_url
    except Exception as e:
        return f"Error retrieving {package_name}: {e}"


def main() -> None:
    pyproject_path = Path("..") / "pyproject.toml"
    deps = get_pyproject_dependencies(pyproject_path)
    repo_urls = {}
    for dep in deps:
        package_name = dep.split()[0] if " " in dep else dep.split(">")[0]
        version: str | None = None
        if "==" in dep:
            parts = dep.split("==")
            package_name = parts[0]
            version = parts[1]
        repo_urls[package_name] = get_pypi_repo_url(package_name, version)
    print("Dependency repository URLs from pyproject.toml:")
    for pkg, url in repo_urls.items():
        print(f"{pkg}: {url}")


if __name__ == "__main__":
    main()
