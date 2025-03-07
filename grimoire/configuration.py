from pathlib import Path

import yaml
from pydantic import BaseModel, HttpUrl


class DBConfiguration(BaseModel):
    """
    TODO: store password in a secure way!
    """

    host: str
    port: int
    user: str
    password: str


class CodeSource(BaseModel):
    url: HttpUrl
    path: str | None


class DocumentSource(BaseModel):
    url: HttpUrl
    site_url: HttpUrl
    exclude: list[str] | None = None
    include: list[str] | None = None


class ProjectConfiguration(BaseModel):
    name: str
    db: DBConfiguration
    docs: list[DocumentSource]
    code: list[CodeSource]

    @classmethod
    def load_from_yaml(cls, path: Path = Path.cwd()) -> "ProjectConfiguration":  # noqa: B008
        with open(path / "grimoire.yaml", encoding="utf-8") as f:
            return cls.model_validate(yaml.safe_load(f))
