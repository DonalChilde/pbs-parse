"""Test api.save.trip_lines."""

from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01 import api as API
from tests.pbs_parse.pbs_2022_01.api import TRIP_LINES_JSON


def test_trip_lines_save_json(test_output_dir: Path):
    """Test saving a trip_lines.json via the api."""
    with resources.as_file(TRIP_LINES_JSON.traversable()) as input_path:
        input_filename = input_path.name
        trip_lines = API.load.trip_lines(
            file_in=input_path, data_type=API.DataType.JSON
        )
    output_dir = test_output_dir / "api-save-triplines"
    path_out = API.save.trip_lines(dir_out=output_dir, trip_lines=trip_lines)
    assert path_out.is_file()
    assert path_out.suffix == ".json"
    assert path_out.name == input_filename
    assert path_out.stat().st_size == 3079


def test_trip_lines_save_yaml(test_output_dir: Path):
    """Test saving a trip_lines.yaml via the api."""
    with resources.as_file(TRIP_LINES_JSON.traversable()) as input_path:
        input_filename = input_path.name
        trip_lines = API.load.trip_lines(
            file_in=input_path, data_type=API.DataType.JSON
        )
    output_dir = test_output_dir / "api-save-triplines"
    path_out = API.save.trip_lines(
        dir_out=output_dir, trip_lines=trip_lines, data_type=API.DataType.YAML
    )
    assert path_out.is_file()
    assert path_out.suffix == ".yaml"
    assert path_out.name == str(Path(input_filename).with_suffix(".yaml"))
    assert path_out.stat().st_size == 2879
