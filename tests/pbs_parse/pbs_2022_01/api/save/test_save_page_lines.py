"""Test api.save.page_lines."""

from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01 import api as API
from tests.pbs_parse.pbs_2022_01.api import PAGE_LINES_JSON


def test_page_lines_save_json(test_output_dir: Path):
    """Test saving a page_lines.json via the api."""
    with resources.as_file(PAGE_LINES_JSON.traversable()) as input_path:
        input_filename = input_path.name
        page_lines = API.load.page_lines(
            file_in=input_path, data_type=API.DataType.JSON
        )
    output_dir = test_output_dir / "api-save-pagelines"
    path_out = API.save.page_lines(dir_out=output_dir, page_lines=page_lines)
    assert path_out.is_file()
    assert path_out.suffix == ".json"
    assert path_out.name == input_filename
    assert path_out.stat().st_size == 18820


def test_page_lines_save_yaml(test_output_dir: Path):
    """Test saving a page_lines.yaml via the api."""
    with resources.as_file(PAGE_LINES_JSON.traversable()) as input_path:
        input_filename = input_path.name
        page_lines = API.load.page_lines(
            file_in=input_path, data_type=API.DataType.JSON
        )
    output_dir = test_output_dir / "api-save-pagelines"
    path_out = API.save.page_lines(
        dir_out=output_dir, page_lines=page_lines, data_type=API.DataType.YAML
    )
    assert path_out.is_file()
    assert path_out.suffix == ".yaml"
    assert path_out.name == str(Path(input_filename).with_suffix(".yaml"))
    assert path_out.stat().st_size == 18620
