from pathlib import Path

import typer

from grimoire.configuration import CONFIG_FILE_NAME, ProjectConfiguration
from grimoire.init import DUMMY_SOURCES

update_cli = typer.Typer()


@update_cli.command(
    "update", help="Update the grimoire sources with the latest dependencies"
)
def update(
    path: Path = typer.Argument(  # noqa: B008
        Path.cwd(),  # noqa: B008
        help="Path to the grimoire project",
    ),
) -> None:
    """
    Update the grimoire sources with the latest dependencies defined in the dependency files.

    :param path: Path to the grimoire project
    """
    config = ProjectConfiguration.load_from_yaml(path / CONFIG_FILE_NAME)

    config.sources = []

    # TODO: add sources from dep files
    for source in DUMMY_SOURCES:
        config.sources.append(source)

    config.save_to_yaml(path / CONFIG_FILE_NAME)
