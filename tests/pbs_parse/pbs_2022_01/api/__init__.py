"""FILE: __init__.py."""

from tests.resources.models.file_system_resource import FileResource

API_RESOURCES = "tests.pbs_parse.pbs_2022_01.api.resources"
PARSED_TRIP_JSON = FileResource(
    anchor=API_RESOURCES, pathname="parsed-trip_2025-03_PHX_00004-02.json"
)
PARSED_TRIP_JSON_2 = FileResource(
    anchor=API_RESOURCES, pathname="parsed-trip_2025-03_PHX_00022-03.json"
)
TRIP_LINES_JSON = FileResource(
    anchor=API_RESOURCES, pathname="trip-lines_2025-03_PHX_00004-02.json"
)
EXPANDED_TRIP_JSON = FileResource(
    anchor=API_RESOURCES, pathname="expanded-trip_2025-03_PHX_320_2025-03-02_10756.json"
)
PAGE_LINES_JSON = FileResource(
    anchor=API_RESOURCES, pathname="page-lines_2025-03_PHX_00009-00.json"
)
