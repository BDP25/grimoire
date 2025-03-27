from pathlib import Path

import yaml
from pydantic import BaseModel

CONFIG_FILE_NAME = "grimoire.yaml"


# see: https://stackoverflow.com/questions/25108581/python-yaml-dump-bad-indentation
class YamlDumper(yaml.Dumper):
    """
    Custom Yaml dumper for list indentation
    """

    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        return super().increase_indent(flow, False)


class LLMConfiguration(BaseModel):
    collection: str
    text_chunk_size: int
    text_chunk_overlap: int
    code_chunk_size: int
    code_chunk_overlap: int


class DBConfiguration(BaseModel):
    """
    TODO: store password in a secure way!
    """

    host: str
    port: int
    user: str
    password: str


class CodeSource(BaseModel):
    url: str


class DocumentSource(BaseModel):
    url: str


class ProjectConfiguration(BaseModel):
    name: str
    db: DBConfiguration
    llm: LLMConfiguration
    docs: list[DocumentSource] | None = None
    code: list[CodeSource] | None = None

    @classmethod
    def load_from_yaml(cls, file_path: Path) -> "ProjectConfiguration":  # noqa: B008
        with open(file_path, encoding="utf-8") as f:
            return cls.model_validate(yaml.safe_load(f))

    def save_to_yaml(self, file_path: Path) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(
                data=self.model_dump(), stream=f, Dumper=YamlDumper, sort_keys=False
            )
