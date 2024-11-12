"""Test cases for the console module."""

import logging

import pytest
from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app

logger = logging.getLogger(__name__)
DATA_FILE_NAME = "ipsum_1.txt"
DATA_FILE_PATH = "files_1"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_app(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_default_options(runner: CliRunner) -> None:
    result = runner.invoke(
        app,
        ["-vvv", "parse", "--help"],
    )
    assert "Verbosity: 3" in result.stdout
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0
