"""Test cli to parse trips."""

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app
from tests.resources.eff_2024_11_01_2024_12_01.LAX import TRIPS_ANCHOR
from tests.resources.models.file_system_resource import FileResource

SINGLE_FILE_TEST = FileResource(
    anchor=TRIPS_ANCHOR,
    pathname=f"trip-lines_LAX_2024-11-01_00001-01.json",
)
DIRECTORY_TEST = FileResource(anchor=TRIPS_ANCHOR, pathname=f"")


def test_parse_trips_file(runner: CliRunner, test_output_dir: Path):  # noqa: D103
    path_out = test_output_dir / "cli" / "parse_trips_file"
    with resources.as_file(SINGLE_FILE_TEST.traversable()) as input_path:
        result = runner.invoke(app, ["manual", "parse", str(input_path), str(path_out)])
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert "found. 1/1" in result.stdout
        assert "error" not in result.stdout


def test_parse_trips_dir(runner: CliRunner, test_output_dir: Path):  # noqa: D103
    path_out = test_output_dir / "cli" / "parse_trips_dir"
    with resources.as_file(DIRECTORY_TEST.traversable()) as input_path:
        result = runner.invoke(app, ["manual", "parse", str(input_path), str(path_out)])
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert "18/18" in result.stdout
        assert "error" not in result.stdout
