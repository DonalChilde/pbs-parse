"""FILE: common.py."""

from enum import StrEnum


class DataType(StrEnum):
    """Possible types of data files."""

    TXT = "txt"
    JSON = "json"
    YAML = "yaml"
