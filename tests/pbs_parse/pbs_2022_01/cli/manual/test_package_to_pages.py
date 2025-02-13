"""Tests for cli, split package to pages."""

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner
from whenever import Date

from pbs_parse.cli.main_typer import app
from tests.pbs_parse.pbs_2022_01.cli import BID_PACKAGE


def test_split_package_to_pages(test_output_dir: Path):
    """test_split_package_to_pages.

    Args:
        runner (CliRunner): _description_
        test_output_dir (Path): _description_
    """
    effective_from = Date(2024, 11, 1)
    effective_to = Date(2024, 12, 1)
    path_out = test_output_dir / "cli-manual" / "package_to_pages"
    with resources.as_file(BID_PACKAGE.traversable()) as input_path:
        result_2 = CliRunner().invoke(
            app,
            [
                "manual",
                "bid-to-pages",
                str(input_path),
                str(path_out),
                "2024-11",
                effective_from.format_common_iso(),
                effective_to.format_common_iso(),
                "LAX",
            ],
        )
        if result_2.stderr_bytes is not None:
            print(result_2.stderr)
        print(result_2.stdout)
        assert result_2.exit_code == 0
        assert "4/1" in result_2.stdout
        assert "error" not in result_2.stdout
        result_files = list(path_out.glob("page-lines*"))
        assert len(result_files) == 4
