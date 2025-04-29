import sys
from pathlib import Path

import typer
import yaml
from pydantic import BaseModel, ConfigDict, ValidationError

from grimoire.helpers.typer import red_text, validation_error

CONFIG_FILE_NAME = "grimoire.yaml"
MODEL_CONFIG_DICT = ConfigDict(extra="forbid")
CONFIG_FILE_RECURSIVE_STEPS = 3


def get_recursive_config(
    path: Path = Path.cwd(),  # noqa: B008
    steps: int = CONFIG_FILE_RECURSIVE_STEPS,
) -> Path:
    """
    Recursive try to find the grimoire.yaml file

    :path: starting path to search
    :steps: number of steps to go up the directory tree
    :return: path to the grimoire.yaml file
    """
    start_path = path
    for _ in range(steps + 1):
        if (path / CONFIG_FILE_NAME).exists():
            return path
        path = path.parent
    typer.echo(
        red_text(
            f"'{CONFIG_FILE_NAME}' not found in '{start_path}' or any of its {steps} parent directories."
        )
    )
    sys.exit(1)


# see: https://stackoverflow.com/questions/25108581/python-yaml-dump-bad-indentation
class YamlDumper(yaml.Dumper):
    """
    Custom Yaml dumper for list indentation
    """

    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        return super().increase_indent(flow, False)


class LLMConfiguration(BaseModel):
    """
    Configuration for the LLM defined and used in the project.
    """

    collection: str
    k_results: int = 5
    score_threshold: float = 0.8
    lambda_mult: float = 0.5
    text_chunk_size: int = 512
    text_chunk_overlap: int = 128
    code_chunk_size: int = 512
    code_chunk_overlap: int = 128

    model_config = MODEL_CONFIG_DICT


class DBConfiguration(BaseModel):
    """
    Configuration for the database defined and used in the project.

    TODO: store password in a secure way!
    """

    host: str
    port: int
    db: str
    user: str
    password: str

    model_config = MODEL_CONFIG_DICT


class Source(BaseModel):
    """
    Representation of a text or code source in the project.
    """

    url: str
    include_md: bool = True
    include_code: bool = False

    model_config = MODEL_CONFIG_DICT


class ProjectConfiguration(BaseModel):
    name: str
    db: DBConfiguration
    llm: LLMConfiguration
    include_project: bool = True
    project_src: str | None = None
    sources: list[Source] | None = None

    model_config = MODEL_CONFIG_DICT

    @classmethod
    def load_from_yaml(cls, file_path: Path) -> "ProjectConfiguration":  # noqa: B008
        """
        Load the project configuration from a YAML file.

        :param file_path: Path to the YAML file.
        :return: ProjectConfiguration instance.
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                return cls.model_validate(yaml.safe_load(f))
        except ValidationError as e:
            typer.echo(validation_error(e))
            raise typer.Exit(code=1) from e

    def save_to_yaml(self, file_path: Path) -> None:
        """
        Save the project configuration to a YAML file.

        :param file_path: Path to the YAML file.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(
                data=self.model_dump(), stream=f, Dumper=YamlDumper, sort_keys=False
            )
