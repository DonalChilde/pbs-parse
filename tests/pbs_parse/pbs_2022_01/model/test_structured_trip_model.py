"""Test for serializing StructuredTrip."""

import json
from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01.models.structured import STRUCTURED_TRIP_SERIALIZER
from tests.resources.eff_2024_11_01_2024_12_01.LAX import STRUCTURED_ANCHOR
from tests.resources.models.file_system_resource import FileResource

SINGLE_FILE_TEST = FileResource(
    anchor=STRUCTURED_ANCHOR,
    pathname=f"structured-trip_LAX_2024-11-01_00001-01.json",
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
