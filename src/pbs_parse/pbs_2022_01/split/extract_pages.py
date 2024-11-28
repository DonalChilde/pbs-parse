"""This module handles splitting a bid package text file into `PageLines`."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from pfmsoft.indexed_string.index_strings import index_lines_in_file
from pfmsoft.indexed_string.model import IndexedString

from pbs_parse.pbs_2022_01.models.split import PageLines, page_lines_serializer


def split_package_to_lines_in_page(
    lines: Iterable[IndexedString],
) -> Iterator[list[IndexedString]]:
    """Collect the lines in each page.

    Args:
        lines: The lines from a bid package.

    Yields:
        The lines in each page.
    """
    accumulated_lines: list[IndexedString] = []
    is_page = False
    for indexed_line in lines:
        if is_page:
            accumulated_lines.append(indexed_line)
        else:
            if "DEPARTURE" in indexed_line.txt:
                is_page = True
                accumulated_lines.append(indexed_line)

        if "COCKPIT" in indexed_line.txt:
            result = accumulated_lines
            accumulated_lines = []
            is_page = False
            yield result


def parse_pages_from_file(path_in: Path) -> Iterator[PageLines]:
    """Get the `PageLines` from a bid package text file.

    Args:
        path_in: The path to a bid package text file.

    Yields:
        The `PageLines`
    """
    reader = index_lines_in_file(file_path=path_in, index_start=1)
    yield from parse_pages(lines=reader)


def parse_pages(lines: Iterator[IndexedString]) -> Iterator[PageLines]:
    """Get the `PageLines` from a collection of `IndexedString`s."""
    for idx, lines_of_page in enumerate(split_package_to_lines_in_page(lines), start=1):
        page = PageLines(idx=idx, lines=lines_of_page)
        yield page


def write_pages(
    file_stem: str, pages: Iterator[PageLines], path_out: Path, overwrite: bool
) -> int:
    """Write the `PageLines` to file with a default file name."""
    pages_list = list(pages)
    count = 0
    serializer = page_lines_serializer()
    for idx, page in enumerate(pages_list, start=1):
        result_path = path_out / Path(
            f"{file_stem}.page_{idx}_of_{len(pages_list)}.json"
        )
        serializer.save_as_json(
            path_out=result_path, complex_obj=page, overwrite=overwrite
        )
        count = idx
    return count
