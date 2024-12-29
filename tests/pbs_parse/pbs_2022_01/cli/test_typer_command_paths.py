"""Test cases for the cli app default path."""

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app


def test_app(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0
    # assert False


def test_default_options(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["-vvv", "debug", "split-to-pages", "--help"])
    assert "Verbosity: 3" in result.stdout
    assert "Debug" in result.stdout
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_pages(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["debug", "split-to-pages", "--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_trips(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["debug", "split-to-trips", "--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_pages_split(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["debug", "split-to-pages", "split", "--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0


def test_trips_split(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["debug", "split-to-trips", "split", "--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0
