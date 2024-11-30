from importlib import resources
from pathlib import Path

from typer.testing import CliRunner

from pbs_parse.cli.main_typer import app
from pbs_parse.pbs_2022_01.split.extract_pages import parse_pages_from_file
from tests.resources import RESOURCES_ANCHOR

DATA_FILE_NAME = "PBS_DCA_May_2022_20220408124308.txt"
DATA_FILE_PATH = "bid_package"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"
PAGE_COUNT = "173"


def test_split_package_to_pages(runner: CliRunner, test_output_dir: Path, capsys):
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    path_out = test_output_dir / "cli" / "package_to_pages"
    with resources.as_file(file_resource) as input_path:
        result = runner.invoke(
            app, ["split-pages", "page", str(input_path), str(path_out)]
        )
        if result.stderr_bytes is not None:
            print(result.stderr)
        with capsys.disabled():
            print(result.stdout)
        assert result.exit_code == 0
        assert PAGE_COUNT in result.stdout


def test_parse_pages():
    # TODO move this test
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    count = 0
    with resources.as_file(file_resource) as input_path:
        for idx, page in enumerate(parse_pages_from_file(path_in=input_path), start=1):
            count = idx
    assert count == 173
