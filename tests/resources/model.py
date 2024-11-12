from dataclasses import dataclass, field
from typing import Any

from pbs_parse.snippets.indexed_string.model import IndexedString


@dataclass
class ParserTest:
    input: IndexedString
    result_id: str
    data: dict[str, Any] = field(default_factory=dict)
    description: str = ""


@dataclass
class GrammarTest:
    txt: str
    description: str = ""
    result: dict[str, Any] = field(default_factory=dict)


@dataclass
class ParseTripTest:
    indexed_anchor: str
    indexed_filename: str
    parsed_anchor: str
    parsed_filename: str
