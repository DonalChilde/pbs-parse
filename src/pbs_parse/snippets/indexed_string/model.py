import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Self, Tuple, TypedDict

from pbs_parse.snippets.file.validate_file_out import validate_file_out


class IndexedStringTD(TypedDict):
    idx: int
    txt: str


class IndexedStringsTD(TypedDict):
    strings: Tuple[IndexedStringTD, ...]


@dataclass(slots=True, frozen=True)
class IndexedString:
    idx: int
    txt: str

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name}(idx={self.idx}, txt={self.txt!r})"

    def __str__(self):
        return f"{self.idx}: {self.txt!r}"

    @classmethod
    def from_dict(cls, data: IndexedStringTD) -> Self:
        return cls(**data)

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        input_string = file_path.read_text(encoding="utf-8")
        input_dict = json.loads(input_string)
        return cls.from_dict(input_dict)

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))


@dataclass(slots=True, frozen=True)
class IndexedStrings:
    strings: Tuple[IndexedString, ...] = ()

    @classmethod
    def from_dict(cls, data: IndexedStringsTD) -> Self:
        return cls(strings=tuple((IndexedString(**x) for x in data.get("strings"))))  # type: ignore

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        input_string = file_path.read_text(encoding="utf-8")
        input_dict = json.loads(input_string)
        return cls.from_dict(input_dict)

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))
