"""Test using the cli to split pages into trips."""

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app
from tests.resources import RESOURCES_ANCHOR

DATA_FILE_PATH = "page"


def test_split_pages_to_trips(runner: CliRunner, test_output_dir: Path, capsys):  # type: ignore
    """Test the cli - convert a directory of pages to trips."""
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_PATH)
    path_out = test_output_dir / "cli" / "pages_to_trips"
    with resources.as_file(file_resource) as input_path:
        result = runner.invoke(
            app, ["split-trips", "all", str(input_path), str(path_out)]
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        with capsys.disabled():  # type: ignore
            print(result.stdout)
        assert result.exit_code == 0
        assert "41 trips found" in result.stdout
