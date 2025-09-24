# pyright: reportUnknownVariableType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportAny=false
# pyright: reportUnknownMemberType=false

import pytest
from typer.testing import CliRunner
from cli import app
import re

runner = CliRunner()


def test_cli_help():
    """Test that the main CLI help command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "FastAPI Application CLI" in result.stdout
    assert "serve" in result.stdout
    assert "version" in result.stdout


def test_serve_help():
    """Test that the serve command help works."""
    result = runner.invoke(app, ["serve", "--help"])
    assert result.exit_code == 0
    assert "Start the FastAPI application server" in result.stdout
    assert "--prod" in result.stdout
    assert "--host" in result.stdout
    assert "--port" in result.stdout
    assert "--workers" in result.stdout
    assert "--log-level" in result.stdout


def test_version_command():
    """Test the version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert re.match(r"[0-9]+\.[0-9]+\.[0-9]+", result.stdout.strip())


def test_invalid_command():
    """Test that invalid commands show appropriate error."""
    result = runner.invoke(app, ["invalid-command"])
    assert result.exit_code != 0
    # Typer puts error messages in stdout when using CliRunner
    assert "No such command" in result.stdout or "No such command" in result.stderr


def test_serve_with_options():
    """Test serve command with various options (without actually starting server)."""
    # Note: This test doesn't actually start the server to avoid port conflicts
    # In a real scenario, you might want to mock uvicorn.run or use a test server

    # Test that the command accepts the options without error
    # We can't easily test the actual server start without mocking uvicorn
    result = runner.invoke(app, ["serve", "--help"])
    assert result.exit_code == 0

    # Verify all expected options are documented
    help_text = result.stdout
    assert "--prod" in help_text
    assert "--host" in help_text
    assert "--port" in help_text
    assert "--workers" in help_text
    assert "--log-level" in help_text


class TestCLICommandStructure:
    """Test the CLI command structure and organization."""

    def test_commands_are_registered(self):
        """Test that all expected commands are registered."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0

        # Check that all main commands are present
        commands = ["serve", "version"]
        for command in commands:
            assert command in result.stdout

    def test_serve_command_description(self):
        """Test that serve command has proper description."""
        result = runner.invoke(app, ["serve", "--help"])
        assert result.exit_code == 0
        assert "Start the FastAPI application server" in result.stdout
        assert "development mode" in result.stdout
        assert "production mode" in result.stdout

    def test_command_help_messages(self):
        """Test that all commands have help messages."""
        commands = ["serve", "version"]

        for command in commands:
            result = runner.invoke(app, [command, "--help"])
            assert result.exit_code == 0, f"Command {command} should have help"
            assert len(result.stdout) > 50, f"Command {command} should have substantial help text"


@pytest.mark.parametrize("command", ["version"])
def test_info_commands(command):
    """Parametrized test for info commands that should run quickly."""
    result = runner.invoke(app, [command])
    assert result.exit_code == 0
    assert len(result.stdout) > 0
