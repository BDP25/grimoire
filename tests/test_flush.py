from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from grimoire.main import cli

runner = CliRunner()


@patch("grimoire.flush.ProjectConfiguration.load_from_yaml")
@patch("grimoire.flush.typer.confirm", return_value=True)
@patch("grimoire.flush.vectorstore_connection")
@patch("grimoire.flush.delete_vectorstore")
@patch("grimoire.flush.typer.echo")
def test_flush_command_success(
    mock_echo, mock_delete, mock_connection, mock_confirm, mock_load
):
    config_mock = MagicMock()
    mock_load.return_value = config_mock
    vectorstore_mock = MagicMock()
    mock_connection.return_value = vectorstore_mock

    result = runner.invoke(cli, ["flush"])

    assert result.exit_code == 0
    mock_load.assert_called_once()
    mock_confirm.assert_called_once()
    mock_connection.assert_called_once_with(config_mock.db)
    mock_delete.assert_called_once_with(vectorstore_mock)
    mock_echo.assert_called_with("Vectorstore flushed")


def test_flush_command_abort():
    result = runner.invoke(cli, ["flush"], input="n\n")
    assert result.exit_code != 0
    assert "Aborted." in result.stdout
