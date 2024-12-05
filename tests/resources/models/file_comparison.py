"""Two file resources in a package.."""

from dataclasses import dataclass

from .file_system_resource import FileResource


@dataclass
class FileComparison:
    """Info needed to locate two files."""

    input: FileResource
    comparison: FileResource
