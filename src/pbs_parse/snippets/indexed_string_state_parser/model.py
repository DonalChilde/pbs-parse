"""Data models for the returns from a parse."""

from dataclasses import dataclass, field
from typing import Any, TypedDict

from . import IndexedString, IndexedStringProtocol, IndexedStringTD
from . import protocol as P


class ParsedIndexedStringTD(TypedDict):
    """ParsedIndexedStringTD.

    Args:
        id (str):
        indexed_string (IndexedStringTD):
        data (dict[str, Any]):
    """

    id: str
    indexed_string: IndexedStringTD
    data: dict[str, Any]


class ParseResultTD(TypedDict):
    """ParseResultTD.

    Args:
        parsed_state (str):
        parsed_indexed_string (ParsedIndexedStringTD):
    """

    parsed_state: str
    parsed_indexed_string: ParsedIndexedStringTD


@dataclass(slots=True)
class ParsedIndexedString:
    """ParsedIndexedString.

    Args:
        id (str):
        indexed_string (IndexedStringProtocol):
        data (dict[str, Any]):
    """

    id: str
    indexed_string: IndexedStringProtocol
    data: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_simple(simple_obj: ParsedIndexedStringTD) -> "ParsedIndexedString":  # noqa: D102
        result = ParsedIndexedString(
            id=simple_obj["id"],
            indexed_string=IndexedString(**simple_obj["indexed_string"]),
            data=simple_obj["data"],
        )
        return result


@dataclass(slots=True)
class ParseResult:
    """ParseResult.

    Args:
        parsed_state (str):
        parsed_indexed_string (P.ParsedIndexedString):
    """

    parsed_state: str
    parsed_indexed_string: P.ParsedIndexedString

    @staticmethod
    def from_simple(simple_obj: ParseResultTD) -> "ParseResult":  # noqa: D102
        result = ParseResult(
            parsed_state=simple_obj["parsed_state"],
            parsed_indexed_string=ParsedIndexedString.from_simple(
                simple_obj["parsed_indexed_string"]
            ),
        )
        return result
