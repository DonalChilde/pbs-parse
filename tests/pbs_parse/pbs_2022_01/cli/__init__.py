"""FILE: __init__.py."""

from tests.resources.models.file_system_resource import FileResource

CLI_RESOURCES = "tests.pbs_parse.pbs_2022_01.cli.resources"

BID_PACKAGE = FileResource(
    anchor=CLI_RESOURCES, pathname="PBS_LAX_November_2024_20241010125833_partial.txt"
)
