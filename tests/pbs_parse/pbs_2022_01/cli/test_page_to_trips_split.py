"""Tests for cli split pages to trips."""

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app
from tests.resources.models.file_system_resource import FileResource
from tests.resources.page_lines import PAGE_LINES_ANCHOR

SINGLE_FILE_TEST = FileResource(
    anchor=PAGE_LINES_ANCHOR,
    pathname=f"2024-11-01_2024-12-01/PBS_LAX_November_2024_20241010125833_partial.page_1_of_4.json",
)
DIRECTORY_TEST = FileResource(
    anchor=PAGE_LINES_ANCHOR, pathname=f"2024-11-01_2024-12-01"
)


def test_split_page_to_trips_file(runner: CliRunner, test_output_dir: Path):  # noqa: D103
    path_out = test_output_dir / "cli" / "page_to_trips_file"
    with resources.as_file(SINGLE_FILE_TEST.traversable()) as input_path:
        result = runner.invoke(
            app, ["split-trips", "trip", str(input_path), str(path_out)]
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        assert result.exit_code == 0
        assert "4 trips found" in result.stdout
        assert "error" not in result.stdout


def test_split_page_to_trips_dir(runner: CliRunner, test_output_dir: Path):  # noqa: D103
    path_out = test_output_dir / "cli" / "page_to_trips_dir"
    with resources.as_file(DIRECTORY_TEST.traversable()) as input_path:
        result = runner.invoke(
            app, ["split-trips", "all", str(input_path), str(path_out)]
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert "18 trips found" in result.stdout
        assert "error" not in result.stdout
