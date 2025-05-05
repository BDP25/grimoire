from pathlib import Path

import typer

from grimoire.configuration import (
    CONFIG_FILE_NAME,
    ProjectConfiguration,
    get_recursive_config,
)

update_cli = typer.Typer()


@update_cli.command(
    "update", help="Update the grimoire sources with the latest dependencies"
)
def update(
    path: Path | None = typer.Option(  # noqa: B008
        None, "--path", help="Path to the grimoire project"
    ),
) -> None:
    """
    Update the grimoire sources with the latest dependencies defined in the dependency files.

    :param path: Path to the grimoire project.
    """
    if path is None:
        path = get_recursive_config()

    config = ProjectConfiguration.load_from_yaml(path / CONFIG_FILE_NAME)

    config.sources = []

    config.save_to_yaml(path / CONFIG_FILE_NAME)
