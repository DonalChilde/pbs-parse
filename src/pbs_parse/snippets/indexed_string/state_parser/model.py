import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Self, TypedDict

from pbs_parse.snippets.file.validate_file_out import validate_file_out
from pbs_parse.snippets.indexed_string.model import IndexedString, IndexedStringTD
from pbs_parse.snippets.indexed_string.protocols import IndexedStringProtocol
from pbs_parse.snippets.indexed_string.state_parser.protocols import (
    ParsedIndexedStringProtocol,
)


class ParsedIndexedStringTD(TypedDict):
    id: str
    indexed_string: IndexedStringTD
    data: dict[str, Any]


class ParsedIndexedStringsTD(TypedDict):
    parsed_strings: list[ParsedIndexedStringTD]


class ParseResultTD(TypedDict):
    current_state: str
    result: ParsedIndexedStringTD


class ParseResultsTD(TypedDict):
    results: list[ParseResultTD]


@dataclass
class ParsedIndexedString:
    id: str
    indexed_string: IndexedStringProtocol
    data: dict[str, Any] = field(default_factory=dict)

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))

    @classmethod
    def from_dict(cls, data: ParsedIndexedStringTD) -> Self:
        return cls(
            id=data["id"],
            indexed_string=IndexedString.from_dict(data["indexed_string"]),
            data=data["data"],
        )

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        input_string = file_path.read_text(encoding="utf-8")
        input_dict = json.loads(input_string)
        return cls.from_dict(input_dict)


@dataclass
class ParsedIndexedStrings:
    parsed_strings: list[ParsedIndexedString] = field(default_factory=list)

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))

    @classmethod
    def from_dict(cls, data: ParsedIndexedStringsTD) -> Self:
        parsed_strings: list[ParsedIndexedString] = []
        for parsed in data["parsed_strings"]:
            parsed_strings.append(ParsedIndexedString.from_dict(parsed))
        return cls(
            parsed_strings=parsed_strings,
        )

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        input_string = file_path.read_text(encoding="utf-8")
        input_dict = json.loads(input_string)
        return cls.from_dict(input_dict)


@dataclass
class ParseResult:
    current_state: str
    result: ParsedIndexedStringProtocol

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))

    @classmethod
    def from_dict(cls, data: ParseResultTD) -> Self:
        return cls(
            current_state=data["current_state"],
            result=ParsedIndexedString.from_dict(data["result"]),
        )

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        input_string = file_path.read_text(encoding="utf-8")
        input_dict = json.loads(input_string)
        return cls.from_dict(input_dict)


@dataclass
class ParseResults:
    results: list[ParseResult] = field(default_factory=list)

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        input_string = file_path.read_text(encoding="utf-8")
        input_dict = json.loads(input_string)
        return cls.from_dict(input_dict)

    @classmethod
    def from_dict(cls, data: ParseResultsTD) -> Self:
        parse_results: list[ParseResult] = []
        for result in data["results"]:
            parse_results.append(ParseResult.from_dict(result))
        return cls(
            results=parse_results,
        )

    def data(self) -> ParsedIndexedStrings:
        parsed = [x.result for x in self.results]
        return ParsedIndexedStrings(parsed_strings=parsed)  # type: ignore
