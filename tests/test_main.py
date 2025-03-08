from typer.testing import CliRunner

from grimoire import __version__
from grimoire.main import cli

runner = CliRunner()


def test_help_flag() -> None:
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "grimoire [OPTIONS] COMMAND [ARGS]..." in result.stdout


def test_includes_commands() -> None:
    result = runner.invoke(cli, ["--help"])
    commands = ["version", "ask", "sync", "verify", "add", "init"]
    for command in commands:
        assert command in result.stdout


def test_command_version() -> None:
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert f"grim cli v{__version__}" in result.stdout
