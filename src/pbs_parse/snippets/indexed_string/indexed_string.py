"""The models for IndexedString, with some generator functions."""

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, TypedDict


class IndexedStringTD(TypedDict):
    """A TypedDict version of IndexedString."""

    idx: int
    txt: str


@dataclass(slots=True)
class IndexedString:
    """A dataclass version of IndexedString."""

    idx: int
    txt: str

    def __repr__(self):  # noqa: D105
        cls_name = self.__class__.__name__
        return f"{cls_name}(idx={self.idx}, txt={self.txt!r})"

    def __str__(self):  # noqa: D105
        return f"{self.idx}: {self.txt!r}"


class IndexedStringProtocol(Protocol):
    """A Protocol version of IndexedString."""

    idx: int
    txt: str


def index_strings(
    strings: Iterable[str],
    string_filter: Callable[[IndexedStringProtocol], bool] | None = None,
    index_start: int = 0,
) -> Iterator[IndexedString]:
    """Enumerate and filter a string iterable, yields an `IndexedString`.

    Args:
        strings (Iterable[str]): _description_
        string_filter (Callable[[IndexedStringProtocol], bool] | None, optional): _description_. Defaults to None.
        index_start (int, optional): _description_. Defaults to 0.

    Yields:
        Iterator[IndexedString]: _description_
    """
    for idx, txt in enumerate(strings, start=index_start):
        indexed_string = IndexedString(idx=idx, txt=txt)
        if string_filter is not None:
            if string_filter(indexed_string):
                yield indexed_string
            else:
                continue
        yield indexed_string


def index_lines_in_file(
    file_path: Path,
    string_filter: Callable[[IndexedStringProtocol], bool] | None = None,
    index_start: int = 1,
) -> Iterator[IndexedString]:
    """Enumerate and filter a text file, yields an `IndexedString`.

    Args:
        file_path (Path): _description_
        string_filter (Callable[[IndexedStringProtocol], bool] | None, optional): _description_. Defaults to None.
        index_start (int, optional): _description_. Defaults to 1.

    Yields:
        Iterator[IndexedString]: _description_
    """
    with open(file_path, encoding="utf-8") as file:
        for idx, line in enumerate(file, start=index_start):
            indexed_string = IndexedString(idx=idx, txt=line)
            if string_filter is not None:
                if string_filter(indexed_string):
                    yield indexed_string
                else:
                    continue
            yield indexed_string
