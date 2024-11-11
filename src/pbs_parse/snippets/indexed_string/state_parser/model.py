import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from pbs_parse.snippets.file.validate_file_out import validate_file_out
from pbs_parse.snippets.indexed_string.protocols import IndexedStringProtocol
from pbs_parse.snippets.indexed_string.state_parser.protocols import (
    ParsedIndexedStringProtocol,
    ParseResultProtocol,
)


@dataclass
class ParsedIndexedString:
    id: str
    indexed_string: IndexedStringProtocol
    data: dict[str, Any] = field(default_factory=dict)

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))


@dataclass
class ParsedIndexedStrings:
    parsed_strings: list[ParsedIndexedString] = field(default_factory=list)

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))


@dataclass
class ParseResult:
    current_state: str
    result: ParsedIndexedStringProtocol

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))


@dataclass
class ParseResults:
    results: list[ParseResultProtocol] = field(default_factory=list)

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))
