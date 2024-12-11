"""Test for serializing PageLines."""

import json
from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01.models.page_lines import PAGE_LINES_SERIALIZER
from tests.resources.models.file_system_resource import FileResource
from tests.resources.page_lines import PAGE_LINES_ANCHOR

SINGLE_FILE_TEST = FileResource(
    anchor=PAGE_LINES_ANCHOR,
    pathname=f"2024-11-01_2024-12-01/PBS_LAX_November_2024_20241010125833_partial.page_1_of_4.json",
)


def test_page_lines_roundtrip(test_output_dir: Path):
    """Test PageLines model will roundtrip to json.

    Args:
        test_output_dir (Path): _description_
    """
    with resources.as_file(SINGLE_FILE_TEST.traversable()) as input_path:
        page_lines = PAGE_LINES_SERIALIZER.load_from_json(path_in=input_path)
        path_out = test_output_dir / "model" / "serialize_page_lines" / input_path.name
    page_lines_json = json.loads(input_path.read_text(encoding="utf-8"))
    page_lines_simple = PAGE_LINES_SERIALIZER.to_simple(page_lines)
    assert page_lines_json == page_lines_simple
    PAGE_LINES_SERIALIZER.save_as_json(path_out=path_out, complex_obj=page_lines)
    page_lines_saved = PAGE_LINES_SERIALIZER.load_from_json(path_in=path_out)
    assert page_lines == page_lines_saved
