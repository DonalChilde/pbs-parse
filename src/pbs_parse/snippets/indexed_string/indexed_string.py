"""The models for IndexedString, with some generator functions."""

from collections.abc import Callable, Iterable, Iterator
from pathlib import Path

from .model import IndexedString, IndexedStringProtocol


def basic_factory(idx: int, txt: str) -> IndexedStringProtocol:
    """A basic default factory that produces dataclass `IndexedString`s."""
    return IndexedString(idx=idx, txt=txt)


def index_strings[T: IndexedStringProtocol](
    strings: Iterable[str],
    string_filter: Callable[[IndexedStringProtocol], bool] | None = None,
    factory: Callable[[int, str], T] = basic_factory,
    index_start: int = 0,
) -> Iterator[T]:
    """Enumerate and filter a string iterable, yields an `IndexedString`.

    Args:
        strings (Iterable[str]): _description_
        string_filter (Callable[[IndexedStringProtocol], bool] | None, optional): _description_. Defaults to None.
        factory (Callable[[int, str], T], optional): _description_. Defaults to basic_factory.
        index_start (int, optional): _description_. Defaults to 0.

    Yields:
        Iterator[IndexedString]: _description_
    """
    for idx, txt in enumerate(strings, start=index_start):
        indexed_string = IndexedString(idx=idx, txt=txt)
        if string_filter is not None:
            if string_filter(indexed_string):
                yield factory(idx, txt)
            else:
                continue
        yield factory(idx, txt)


def index_lines_in_file[T: IndexedStringProtocol](
    file_path: Path,
    string_filter: Callable[[IndexedStringProtocol], bool] | None = None,
    factory: Callable[[int, str], T] = basic_factory,
    index_start: int = 1,
) -> Iterator[T]:
    """Enumerate and filter a text file, yields an `IndexedString`.

    Args:
        file_path (Path): _description_
        string_filter (Callable[[IndexedStringProtocol], bool] | None, optional): _description_. Defaults to None.
        factory (Callable[[int, str], T], optional): _description_. Defaults to basic_factory.
        index_start (int, optional): _description_. Defaults to 1.

    Yields:
        Iterator[IndexedString]: _description_
    """
    with open(file_path, encoding="utf-8") as file:
        for idx, line in enumerate(file, start=index_start):
            indexed_string = IndexedString(idx=idx, txt=line)
            if string_filter is not None:
                if string_filter(indexed_string):
                    yield factory(idx, line)
                else:
                    continue
            yield factory(idx, line)
