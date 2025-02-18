"""Models for IndexedString using vanilla python."""

from dataclasses import dataclass
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
