"""State parser test data."""

from dataclasses import dataclass

from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser.abc import ParserABC

# TODO decide how to represent parse result...


@dataclass(slots=True)
class StateParserTest[T]:
    """Parser test."""

    input: IndexedString
    parser: ParserABC
    result_id: str
    data: T
    description: str = ""
