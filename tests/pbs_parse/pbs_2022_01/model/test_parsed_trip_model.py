"""Test for serializing ParsedTrip."""

import json
from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER
from tests.resources.models.file_system_resource import FileResource
from tests.resources.parsed_trips import PARSED_TRIPS_ANCHOR

SINGLE_FILE_TEST = FileResource(
    anchor=PARSED_TRIPS_ANCHOR,
    pathname=f"2024-11-01_2024-12-01/parsed-trip_page_1_trip_4_9726d2fb-4892-5e06-b43b-360c3f347874.json",
)


def test_parsed_trip_roundtrip(test_output_dir: Path):
    """Test ParsedTrip model will roundtrip to json.

    Args:
        test_output_dir (Path): _description_
    """
    with resources.as_file(SINGLE_FILE_TEST.traversable()) as input_path:
        parsed_trip = PARSED_TRIP_SERIALIZER.load_from_json(path_in=input_path)
        path_out = test_output_dir / "model" / "serialize_parsed_trip" / input_path.name
    parsed_trip_json = json.loads(input_path.read_text(encoding="utf-8"))
    parsed_trip_simple = PARSED_TRIP_SERIALIZER.to_simple(parsed_trip)
    assert parsed_trip_json == parsed_trip_simple
    PARSED_TRIP_SERIALIZER.save_as_json(path_out=path_out, complex_obj=parsed_trip)
    parsed_trip_saved = PARSED_TRIP_SERIALIZER.load_from_json(path_in=path_out)
    assert parsed_trip == parsed_trip_saved
