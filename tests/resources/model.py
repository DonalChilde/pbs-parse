from dataclasses import dataclass, field
from typing import Any

from pfmsoft.snippets.indexed_string.model import IndexedString


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
class FileBasedTest:
    input_anchor: str
    input_filename: str
    comparison_anchor: str
    comparison_filename: str
