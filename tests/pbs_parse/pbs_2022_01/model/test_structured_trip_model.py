"""Test for serializing StructuredTrip."""

import json
from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01.models.structured import STRUCTURED_TRIP_SERIALIZER
from tests.resources.models.file_system_resource import FileResource
from tests.resources.structured_trips import STRUCTURED_TRIPS_ANCHOR

SINGLE_FILE_TEST = FileResource(
    anchor=STRUCTURED_TRIPS_ANCHOR,
    pathname=f"2024-11-01_2024-12-01/PBS_LAX_November_2024_20241010125833_partial.page_1_of_4.trip_1_of_4.parsed.structured.json",
)


def test_structured_trip_roundtrip(test_output_dir: Path):
    """Test StructuredTrip model will roundtrip to json.

    Args:
        test_output_dir (Path): _description_
    """
    with resources.as_file(SINGLE_FILE_TEST.traversable()) as input_path:
        structured_trip = STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=input_path)
        path_out = (
            test_output_dir / "model" / "serialize_structured_trip" / input_path.name
        )
    structured_trip_json = json.loads(input_path.read_text(encoding="utf-8"))
    structured_trip_simple = STRUCTURED_TRIP_SERIALIZER.to_simple(structured_trip)
    assert structured_trip_json == structured_trip_simple
    STRUCTURED_TRIP_SERIALIZER.save_as_json(
        path_out=path_out, complex_obj=structured_trip
    )
    structured_trip_saved = STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=path_out)
    assert structured_trip == structured_trip_saved
