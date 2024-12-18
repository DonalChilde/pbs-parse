"""Test cli to structure parsed trips."""

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app
from tests.resources.models.file_system_resource import FileResource
from tests.resources.parsed_trips import PARSED_TRIPS_ANCHOR

SINGLE_FILE_TEST = FileResource(
    anchor=PARSED_TRIPS_ANCHOR,
    pathname=f"2024-11-01_2024-12-01/PBS_LAX_November_2024_20241010125833_partial.page_1_of_4.trip_1_of_4.parsed.json",
)
DIRECTORY_TEST = FileResource(
    anchor=PARSED_TRIPS_ANCHOR, pathname=f"2024-11-01_2024-12-01"
)


def test_structure_trips_file(runner: CliRunner, test_output_dir: Path):  # noqa: D103
    path_out = test_output_dir / "cli" / "structure_trips_file"
    with resources.as_file(SINGLE_FILE_TEST.traversable()) as input_path:
        result = runner.invoke(
            app,
            [
                "debug",
                "structure",
                "trip",
                str(input_path),
                str(path_out),
                "2024-11-01",
                "2024-12-01",
            ],
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert "1 of 1, 1 trips found" in result.stdout
        assert "error" not in result.stdout


def test_structure_trips_dir(runner: CliRunner, test_output_dir: Path):  # noqa: D103
    path_out = test_output_dir / "cli" / "structure_trips_dir"
    with resources.as_file(DIRECTORY_TEST.traversable()) as input_path:
        result = runner.invoke(
            app,
            [
                "debug",
                "structure",
                "all",
                str(input_path),
                str(path_out),
                "2024-11-01",
                "2024-12-01",
            ],
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert "18 of 18, 18 trips found" in result.stdout
        assert "error" not in result.stdout
