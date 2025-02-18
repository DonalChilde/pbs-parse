"""Models for IndexedString using vanilla python."""

from pydantic import BaseModel


class IndexedString(BaseModel):
    """A pydantic version of IndexedString."""

    idx: int
    txt: str

    def __repr__(self):  # noqa: D105
        cls_name = self.__class__.__name__
        return f"{cls_name}(idx={self.idx}, txt={self.txt!r})"

    def __str__(self):  # noqa: D105
        return f"{self.idx}: {self.txt!r}"


def pydantic_factory(idx: int, txt: str) -> IndexedString:
    """A factory returning a pydantic IndexedString."""
    return IndexedString(idx=idx, txt=txt)
