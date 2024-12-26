"""Test cli to parse trips."""

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app
from tests.resources.models.file_system_resource import FileResource
from tests.resources.trip_lines import TRIP_LINES_ANCHOR

SINGLE_FILE_TEST = FileResource(
    anchor=TRIP_LINES_ANCHOR,
    pathname=f"2024-11-01_2024-12-01/trip-lines_page_1_trip_1_2565ba54-18cd-53d1-a4d1-6155478cb42e.json",
)
DIRECTORY_TEST = FileResource(
    anchor=TRIP_LINES_ANCHOR, pathname=f"2024-11-01_2024-12-01"
)


def test_parse_trips_file(runner: CliRunner, test_output_dir: Path):  # noqa: D103
    path_out = test_output_dir / "cli" / "parse_trips_file"
    with resources.as_file(SINGLE_FILE_TEST.traversable()) as input_path:
        result = runner.invoke(
            app, ["debug", "parse", "trip", str(input_path), str(path_out)]
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert "1 of 1, 1 trips parsed" in result.stdout
        assert "error" not in result.stdout


def test_parse_trips_dir(runner: CliRunner, test_output_dir: Path):  # noqa: D103
    path_out = test_output_dir / "cli" / "parse_trips_dir"
    with resources.as_file(DIRECTORY_TEST.traversable()) as input_path:
        result = runner.invoke(
            app, ["debug", "parse", "all-trips", str(input_path), str(path_out)]
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert "18 of 18, 18 trips parsed" in result.stdout
        assert "error" not in result.stdout
