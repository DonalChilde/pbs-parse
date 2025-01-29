"""FILE: test_expand_debug.py."""

from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01 import api as API
from tests.resources import RESOURCES_ANCHOR
from tests.resources.models.file_system_resource import FileResource

DEBUG_FILE = FileResource(
    anchor=f"{RESOURCES_ANCHOR}.parsed",
    pathname="parsed-trip_LAX_2024-03-02_00021-02.json",
)


def test_expand(test_output_dir: Path):
    """test_expand.

    Args:
        test_output_dir (Path): _description_
    """
    path_out = test_output_dir / "api" / "expand_debug"
    with resources.as_file(DEBUG_FILE.traversable()) as input_path:
        parsed = API.load.parsed_trip(file_in=input_path)
        expanded_trips = list(
            API.transform.parsed_to_expanded(parsed_trips=[parsed], debug_dir=path_out)
        )

        assert len(expanded_trips) == 1
