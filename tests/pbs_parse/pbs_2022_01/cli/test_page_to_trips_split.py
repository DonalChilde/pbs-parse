from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app
from tests.resources import RESOURCES_ANCHOR

DATA_FILE_NAME = "PBS_DCA_May_2022_20220408124308.page_1_of_173.json"
DATA_FILE_PATH = "page"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"


def test_split_page_to_trips(runner: CliRunner, test_output_dir: Path, capsys):
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    path_out = test_output_dir / "cli" / "page_to_trips"
    with resources.as_file(file_resource) as input_path:
        result = runner.invoke(app, ["trips", "split", str(input_path), str(path_out)])
        if result.stderr_bytes is not None:
            print(result.stderr)
        with capsys.disabled():
            print(result.stdout)
        assert result.exit_code == 0
        assert "7 trips found" in result.stdout
