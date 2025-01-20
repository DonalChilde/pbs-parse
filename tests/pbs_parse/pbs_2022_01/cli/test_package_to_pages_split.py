"""Tests for cli, split package to pages."""

from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app
from tests.resources.eff_2024_11_01_2024_12_01.LAX import BID_PACKAGE_ANCHOR
from tests.resources.models.file_system_resource import FileResource


@dataclass
class PackageToPagesTest:
    """PackageToPagesTest."""

    effective_from: str
    effective_to: str
    input: FileResource
    base: str = ""

    def date_path(self) -> str:
        """date_path.

        Returns:
            str: _description_
        """
        return f"{self.effective_from}_{self.effective_to}"


SINGLE_FILE_TEST = PackageToPagesTest(
    effective_from="2024-11-01",
    effective_to="2024-12-01",
    input=FileResource(
        anchor=BID_PACKAGE_ANCHOR,
        pathname=f"PBS_LAX_November_2024_20241010125833_partial.txt",
    ),
)
DIRECTORY_TEST = PackageToPagesTest(
    effective_from="2024-11-01",
    effective_to="2024-12-01",
    input=FileResource(anchor=BID_PACKAGE_ANCHOR, pathname=""),
)


def test_split_package_to_pages_file(runner: CliRunner, test_output_dir: Path):
    """test_split_package_to_pages_file.

    Args:
        runner (CliRunner): _description_
        test_output_dir (Path): _description_
    """
    path_out = (
        test_output_dir / "cli" / "package_to_pages_file" / SINGLE_FILE_TEST.date_path()
    )
    with resources.as_file(SINGLE_FILE_TEST.input.traversable()) as input_path:
        result = runner.invoke(
            app,
            [
                "manual",
                "split-to-pages",
                str(input_path),
                str(path_out),
                SINGLE_FILE_TEST.effective_from,
                SINGLE_FILE_TEST.effective_to,
            ],
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
    path_out = (
        test_output_dir / "cli" / "package_to_pages_dir" / DIRECTORY_TEST.date_path()
    )
    with resources.as_file(DIRECTORY_TEST.input.traversable()) as input_path:
        result = runner.invoke(
            app,
            [
                "manual",
                "split-to-pages",
                str(input_path),
                str(path_out),
                DIRECTORY_TEST.effective_from,
                DIRECTORY_TEST.effective_to,
            ],
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert "to 4 pages" in result.stdout
        assert "error" not in result.stdout
