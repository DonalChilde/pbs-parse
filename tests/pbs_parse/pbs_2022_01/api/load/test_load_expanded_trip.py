"""Test api.load.expanded_trip."""

from importlib import resources

from pbs_parse.pbs_2022_01 import api as API
from tests.pbs_parse.pbs_2022_01.api import EXPANDED_TRIP_JSON


def test_page_lines_load_json():
    """Test loading a page_lines.json via the api."""
    with resources.as_file(EXPANDED_TRIP_JSON.traversable()) as input_path:
        expanded_trip = API.load.expanded_trip(
            file_in=input_path, data_type=API.DataType.JSON
        )
    assert expanded_trip.bid.base == "PHX"
    assert expanded_trip.bid.name == "2025-03"
    assert len(expanded_trip.dutyperiods) == 3
    assert expanded_trip.trip_number == "10756"
