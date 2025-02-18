"""A Pydantic BaseModel version of ParseResult."""

from typing import Any

from pydantic import BaseModel

from . import PM


class ParsedIndexedString(BaseModel):
    """ParsedIndexedString.

    Args:
        id (str):
        indexed_string (IndexedStringProtocol):
        data (dict[str, Any]):
    """

    id: str
    indexed_string: PM.IndexedString
    data: dict[str, Any]


class ParseResult(BaseModel):
    """ParseResult.

    Args:
        parsed_state (str):
        parsed_indexed_string (ParsedIndexedString):
    """

    parsed_state: str
    parsed_indexed_string: ParsedIndexedString
