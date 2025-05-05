import yaml
from typer.testing import CliRunner

from grimoire.configuration import CONFIG_FILE_NAME
from grimoire.main import cli

runner = CliRunner()


def test_verify_command_no_config_file(tmp_path):
    result = runner.invoke(cli, ["verify", "--path", str(tmp_path)])
    assert result.exit_code == 1
    assert "No configuration file found" in result.output


def test_verify_command_with_valid_config(tmp_path, config_data):
    config_path = tmp_path / CONFIG_FILE_NAME
    with config_path.open("w") as f:
        yaml.dump(config_data, f)

    result = runner.invoke(cli, ["verify", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "Verifying configuration" in result.output
    assert "Successful for: test_project" in result.output


def test_verify_command_with_extra_config_raises_error(tmp_path, config_data):
    config_data["extra_data"] = "Invalid"
    config_path = tmp_path / CONFIG_FILE_NAME
    with config_path.open("w") as f:
        yaml.dump(config_data, f)

    result = runner.invoke(cli, ["verify", "--path", str(tmp_path)])

    assert result.exit_code == 1
    assert "Error in configuration file" in result.output
    assert "extra_data" in result.output
