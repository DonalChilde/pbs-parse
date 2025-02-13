"""Test api.load.pages_lines."""

from importlib import resources

from pbs_parse.pbs_2022_01 import api as API
from tests.pbs_parse.pbs_2022_01.api import PAGE_LINES_JSON


def test_page_lines_load_json():
    """Test loading a page_lines.json via the api."""
    with resources.as_file(PAGE_LINES_JSON.traversable()) as input_path:
        page_lines = API.load.page_lines(
            file_in=input_path, data_type=API.DataType.JSON
        )
    assert page_lines.bid.base == "PHX"
    assert page_lines.bid.name == "2025-03"
    assert len(page_lines.lines) == 79
    assert page_lines.idx == "00009-00"
