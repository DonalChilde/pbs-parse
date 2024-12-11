"""Test for serializing TripLines."""

import json
from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01.models.trip_lines import TRIP_LINES_SERIALIZER
from tests.resources.models.file_system_resource import FileResource
from tests.resources.trip_lines import TRIP_LINES_ANCHOR

SINGLE_FILE_TEST = FileResource(
    anchor=TRIP_LINES_ANCHOR,
    pathname=f"2024-11-01_2024-12-01/PBS_LAX_November_2024_20241010125833_partial.page_1_of_4.trip_1_of_4.json",
)


def test_page_lines_roundtrip(test_output_dir: Path):
    """Test TripLines model will roundtrip to json.

    Args:
        test_output_dir (Path): _description_
    """
    with resources.as_file(SINGLE_FILE_TEST.traversable()) as input_path:
        trip_lines = TRIP_LINES_SERIALIZER.load_from_json(path_in=input_path)
        path_out = test_output_dir / "model" / "serialize_trip_lines" / input_path.name
    trip_lines_json = json.loads(input_path.read_text(encoding="utf-8"))
    trip_lines_simple = TRIP_LINES_SERIALIZER.to_simple(trip_lines)
    assert trip_lines_json == trip_lines_simple
    TRIP_LINES_SERIALIZER.save_as_json(path_out=path_out, complex_obj=trip_lines)
    trip_lines_saved = TRIP_LINES_SERIALIZER.load_from_json(path_in=path_out)
    assert trip_lines == trip_lines_saved
