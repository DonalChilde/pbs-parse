"""Test api.load.trip_lines."""

from importlib import resources

from pbs_parse.pbs_2022_01 import api as API
from tests.pbs_parse.pbs_2022_01.api import TRIP_LINES_JSON


def test_trip_lines_load_json():
    """Test loading a page_lines.json via the api."""
    with resources.as_file(TRIP_LINES_JSON.traversable()) as input_path:
        trip_lines = API.load.trip_lines(
            file_in=input_path, data_type=API.DataType.JSON
        )
    assert trip_lines.bid.base == "PHX"
    assert trip_lines.bid.name == "2025-03"
    assert len(trip_lines.lines) == 17
    assert trip_lines.idx == "00004-02"
