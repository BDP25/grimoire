from pathlib import Path

import yaml
from pydantic import BaseModel, HttpUrl

CONFIG_FILE_NAME = "grimoire.yaml"


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
    docs: list[DocumentSource] | None = None
    code: list[CodeSource] | None = None

    @classmethod
    def load_from_yaml(cls, file_path: Path) -> "ProjectConfiguration":  # noqa: B008
        with open(file_path, encoding="utf-8") as f:
            return cls.model_validate(yaml.safe_load(f))

    def save_to_yaml(self, file_path: Path) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(self.model_dump(), f, sort_keys=False)
