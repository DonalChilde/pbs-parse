"""Test cases for the cli app default path."""

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app


def test_app() -> None:
    """It exits with a status code of zero."""
    result = CliRunner().invoke(app, ["--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0
    # assert False


def test_default_options() -> None:
    """It exits with a status code of zero."""
    result = CliRunner().invoke(app, ["-vvv", "manual", "--help"])
    assert "Verbosity: 3" in result.stdout
    assert "Debug" in result.stdout
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_pages() -> None:
    """It exits with a status code of zero."""
    result = CliRunner().invoke(app, ["manual", "bid-to-pages", "--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_trips() -> None:
    """It exits with a status code of zero."""
    result = CliRunner().invoke(app, ["manual", "pages-to-trips", "--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0
