from pathlib import Path
from typing import Callable, Iterable, Iterator

from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.protocols import IndexedStringProtocol


def index_strings(
    strings: Iterable[str],
    string_filter: Callable[[IndexedStringProtocol], bool] | None = None,
    index_start: int = 0,
) -> Iterator[IndexedStringProtocol]:
    """
    Enumerate and filter a string iterable, yield matches as an `IndexedString`

    Args:
        strings: An iterable of strings.
        string_filter: Used to test strings.
        index_start: Defaults to 0.

    Yields:
        The matched indexed strings.
    """
    for idx, txt in enumerate(strings, start=index_start):
        indexed_string = IndexedString(idx=idx, txt=txt)
        if string_filter is not None:
            if string_filter(indexed_string):
                yield indexed_string
        yield indexed_string


def index_file_line(
    file_path: Path,
    string_filter: Callable[[IndexedStringProtocol], bool] | None = None,
    index_start: int = 0,
) -> Iterator[IndexedStringProtocol]:
    with open(file_path, encoding="utf-8") as file:
        for idx, line in enumerate(file, start=index_start):
            indexed_string = IndexedString(idx=idx, txt=line)
            if string_filter is not None:
                if string_filter(indexed_string):
                    yield indexed_string
            yield indexed_string
