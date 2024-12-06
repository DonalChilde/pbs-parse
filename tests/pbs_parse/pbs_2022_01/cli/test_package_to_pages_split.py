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


def test_split_package_to_pages_file(runner: CliRunner, test_output_dir: Path):  # noqa: D103
    path_out = test_output_dir / "cli" / "package_to_pages_file"
    with resources.as_file(SINGLE_FILE_TEST.traversable()) as input_path:
        result = runner.invoke(
            app, ["split-pages", "page", str(input_path), str(path_out)]
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        assert result.exit_code == 0
        assert "4 pages found" in result.stdout


def test_split_package_to_pages_dir(runner: CliRunner, test_output_dir: Path):  # noqa: D103
    path_out = test_output_dir / "cli" / "package_to_pages_dir"
    with resources.as_file(DIRECTORY_TEST.traversable()) as input_path:
        result = runner.invoke(
            app, ["split-pages", "all", str(input_path), str(path_out)]
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        assert result.exit_code == 0
        assert "4 pages found" in result.stdout


# def test_parse_pages():
#     # TODO move this test
#     file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
#     count = 0
#     with resources.as_file(file_resource) as input_path:
#         for idx, page in enumerate(parse_pages_from_file(path_in=input_path), start=1):
#             count = idx
#     assert count == 173
