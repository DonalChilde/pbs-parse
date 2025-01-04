"""Tests for cli, split package to pages."""

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app
from tests.resources.bid_package import BID_PACKAGE_ANCHOR
from tests.resources.models.file_system_resource import FileResource

SINGLE_FILE_TEST = FileResource(
    anchor=BID_PACKAGE_ANCHOR,
    pathname=f"2024-11-01_2024-12-01/PBS_LAX_November_2024_20241010125833_partial.txt",
)
DIRECTORY_TEST = FileResource(
    anchor=BID_PACKAGE_ANCHOR, pathname=f"2024-11-01_2024-12-01"
)


def test_split_package_to_pages_file(runner: CliRunner, test_output_dir: Path):
    """test_split_package_to_pages_file.

    Args:
        runner (CliRunner): _description_
        test_output_dir (Path): _description_
    """
    path_out = test_output_dir / "cli" / "package_to_pages_file"
    with resources.as_file(SINGLE_FILE_TEST.traversable()) as input_path:
        result = runner.invoke(
            app, ["manual", "split-to-pages", str(input_path), str(path_out)]
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert "to 4 pages" in result.stdout
        assert "error" not in result.stdout


def test_split_package_to_pages_dir(runner: CliRunner, test_output_dir: Path):
    """test_split_package_to_pages_dir.

    Args:
        runner (CliRunner): _description_
        test_output_dir (Path): _description_
    """
    path_out = test_output_dir / "cli" / "package_to_pages_dir"
    with resources.as_file(DIRECTORY_TEST.traversable()) as input_path:
        result = runner.invoke(
            app,
            ["debug", "packages", "split", str(input_path), str(path_out)],
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert "4 pages found" in result.stdout
        assert "error" not in result.stdout
