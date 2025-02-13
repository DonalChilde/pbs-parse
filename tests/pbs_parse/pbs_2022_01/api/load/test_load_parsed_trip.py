"""Test api.load.parsed_trip."""

from importlib import resources

from pbs_parse.pbs_2022_01 import api as API
from tests.pbs_parse.pbs_2022_01.api import PARSED_TRIP_JSON


def test_page_lines_load_json():
    """Test loading a page_lines.json via the api."""
    with resources.as_file(PARSED_TRIP_JSON.traversable()) as input_path:
        parsed_trip = API.load.parsed_trip(
            file_in=input_path, data_type=API.DataType.JSON
        )
    assert parsed_trip.bid.base == "PHX"
    assert parsed_trip.bid.name == "2025-03"
    assert len(parsed_trip.parsed_lines) == 17
    assert parsed_trip.idx == "00004-02"
    assert parsed_trip.parsed_lines[2].data["trip_number"] == "10652"
