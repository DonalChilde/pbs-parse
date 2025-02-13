"""Test api.save.expanded_trip."""

from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01 import api as API
from tests.pbs_parse.pbs_2022_01.api import EXPANDED_TRIP_JSON


def test_expanded_trip_save_json(test_output_dir: Path):
    """Test saving an expanded_trip.json via the api."""
    with resources.as_file(EXPANDED_TRIP_JSON.traversable()) as input_path:
        input_filename = input_path.name
        expanded_trip = API.load.expanded_trip(
            file_in=input_path, data_type=API.DataType.JSON
        )
    output_dir = test_output_dir / "api-save-expandedtrip"
    path_out = API.save.expanded_trip(dir_out=output_dir, expanded_trip=expanded_trip)
    assert path_out.is_file()
    assert path_out.suffix == ".json"
    assert path_out.name == input_filename
    assert path_out.stat().st_size == 7327


def test_expanded_trip_save_yaml(test_output_dir: Path):
    """Test saving an expanded_trip.yaml via the api."""
    with resources.as_file(EXPANDED_TRIP_JSON.traversable()) as input_path:
        input_filename = input_path.name
        expanded_trip = API.load.expanded_trip(
            file_in=input_path, data_type=API.DataType.JSON
        )
    output_dir = test_output_dir / "api-save-expandedtrip"
    path_out = API.save.expanded_trip(
        dir_out=output_dir, expanded_trip=expanded_trip, data_type=API.DataType.YAML
    )
    assert path_out.is_file()
    assert path_out.suffix == ".yaml"
    assert path_out.name == str(Path(input_filename).with_suffix(".yaml"))
    assert path_out.stat().st_size == 5765
