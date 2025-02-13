"""Test api.save.parsed_trip."""

from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01 import api as API
from tests.pbs_parse.pbs_2022_01.api import PARSED_TRIP_JSON


def test_parsed_trip_save_json(test_output_dir: Path):
    """Test saving a parsed_trip.json via the api."""
    with resources.as_file(PARSED_TRIP_JSON.traversable()) as input_path:
        input_filename = input_path.name
        parsed_trip = API.load.parsed_trip(
            file_in=input_path, data_type=API.DataType.JSON
        )
    output_dir = test_output_dir / "api-save-parsedtrip"
    path_out = API.save.parsed_trip(dir_out=output_dir, parsed_trip=parsed_trip)
    assert path_out.is_file()
    assert path_out.suffix == ".json"
    assert path_out.name == input_filename
    assert path_out.stat().st_size == 10144


def test_parsed_trip_save_yaml(test_output_dir: Path):
    """Test saving a parsed_trip.yaml via the api."""
    with resources.as_file(PARSED_TRIP_JSON.traversable()) as input_path:
        input_filename = input_path.name
        parsed_trip = API.load.parsed_trip(
            file_in=input_path, data_type=API.DataType.JSON
        )
    output_dir = test_output_dir / "api-save-parsedtrip"
    path_out = API.save.parsed_trip(
        dir_out=output_dir, parsed_trip=parsed_trip, data_type=API.DataType.YAML
    )
    assert path_out.is_file()
    assert path_out.suffix == ".yaml"
    assert path_out.name == str(Path(input_filename).with_suffix(".yaml"))
    assert path_out.stat().st_size == 8775
