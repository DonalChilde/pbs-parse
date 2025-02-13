"""Test api.save.expanded_debug."""

from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01 import api as API
from tests.pbs_parse.pbs_2022_01.api import EXPANDED_TRIP_JSON, PARSED_TRIP_JSON_2


def test_expanded_trip_save_json(test_output_dir: Path):
    """Test saving an expanded_trip.json via the api."""
    with resources.as_file(EXPANDED_TRIP_JSON.traversable()) as input_path:
        expanded_trip = API.load.expanded_trip(
            file_in=input_path, data_type=API.DataType.JSON
        )
    with resources.as_file(PARSED_TRIP_JSON_2.traversable()) as input_path:
        parsed_trip = API.load.parsed_trip(file_in=input_path)
    output_dir = test_output_dir / "api-save-expandeddebug"
    path_out_json = API.save.expanded_debug(
        dir_out=output_dir, expanded=expanded_trip, parsed=parsed_trip
    )
    path_out_txt = path_out_json.with_suffix(".txt")

    assert path_out_json.is_file()
    assert path_out_json.name.endswith("debug.json")
    assert path_out_json.stat().st_size == 19768

    assert path_out_txt.is_file()
    assert path_out_txt.suffix == ".txt"
    assert path_out_txt.name.endswith("debug.txt")
    assert path_out_txt.stat().st_size == 17923
