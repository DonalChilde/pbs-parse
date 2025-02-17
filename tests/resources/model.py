"""Models used in testing."""

from dataclasses import dataclass, field
from typing import Any

from pbs_parse.snippets.indexed_string import IndexedString


@dataclass
class ParserTest:
    """Parser test."""

    # update to generic?
    input: IndexedString
    result_id: str
    data: dict[str, Any] = field(default_factory=dict)
    description: str = ""


@dataclass
class ParserTest2[T]:
    """Parser test."""

    input: IndexedString
    result_id: str
    data: T
    description: str = ""


@dataclass
class GrammarTest:
    """Old style grammar test."""

    txt: str
    description: str = ""
    result: dict[str, Any] = field(default_factory=dict)


@dataclass
class FileBasedTest:
    """Info needed to locate two files."""

    input_anchor: str
    input_filename: str
    comparison_anchor: str
    comparison_filename: str


@dataclass
class ParsingTest[T]:
    """Contains input and result data for a test."""

    txt: str
    result: T
    description: str = ""
