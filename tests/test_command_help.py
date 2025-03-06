from typer.testing import CliRunner

from grimoire.cli import cli

runner = CliRunner()


def test_help_command() -> None:
    result = runner.invoke(cli, ["help"])
    assert result.exit_code == 0
    assert "grimoire [OPTIONS] COMMAND [ARGS]..." in result.stdout


def test_help_flag() -> None:
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "grimoire [OPTIONS] COMMAND [ARGS]..." in result.stdout


def test_includes_commands() -> None:
    result = runner.invoke(cli, ["help"])
    commands = ["init", "add", "sync", "ask", "help"]
    for command in commands:
        assert command in result.stdout
