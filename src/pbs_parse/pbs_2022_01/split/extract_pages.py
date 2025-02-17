"""This module handles splitting a bid package text file into `PageLines`."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from pbs_parse.pbs_2022_01.models.bid_data import BidData
from pbs_parse.pbs_2022_01.models.page_lines import (
    PageLines,
    PageLinesSource,
    page_lines_serializer,
)
from pbs_parse.snippets.indexed_string import IndexedString, index_lines_in_file

# def split_to_pages(
#     path_in: Path,
#     bid: BidData,
#     observer: Callable[[PageLines], None] | None = None,
# ) -> Iterator[PageLines]:
#     """Split a text file to PageLines, with an optional observer.

#     Args:
#         path_in (Path): The path to the input text file.
#         bid (BidData): Base and effective date info.
#         observer (Callable[[PageLines], None] | None, optional): The optional observer.
#             Defaults to None.

#     Yields:
#         Iterator[PageLines]: _description_
#     """
#     reader = index_lines_in_file(file_path=path_in, index_start=1)
#     for page in parse_page_lines(source=path_in.name, bid=bid, lines=reader):
#         if observer:
#             observer(page)
#         yield page


def lines_of_package_to_lines_of_pages(
    lines: Iterable[IndexedString],
) -> Iterator[list[IndexedString]]:
    """Collect the lines in each page.

    Args:
        lines (Iterable[IndexedString]): The lines from a bid package.

    Yields:
        Iterator[list[IndexedString]]: The lines in each page.
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


def parse_page_lines_from_file(path_in: Path, bid: BidData) -> Iterator[PageLines]:
    """Get the `PageLines` from a bid package text file.

    Args:
        path_in (Path): The path to a bid package text file.
        bid (BidData): Base and effective date info.

    Yields:
        Iterator[PageLines]: The `PageLines`
    """
    reader = index_lines_in_file(file_path=path_in, index_start=1)
    yield from parse_page_lines(source=path_in.name, bid=bid, lines=reader)


def parse_page_lines(
    lines: Iterator[IndexedString], source: str, bid: BidData
) -> Iterator[PageLines]:
    """Get the `PageLines` from a collection of `IndexedString`s.

    Args:
        lines (Iterator[IndexedString]): The lines from a bid package.
        source (str): The file name of the source txt file.
        bid (BidData): Base and effective date info.

    Yields:
        Iterator[PageLines]: The PageLines.
    """
    for idx, lines_of_page in enumerate(
        lines_of_package_to_lines_of_pages(lines), start=1
    ):
        _source = PageLinesSource(txt_file=source)
        page = PageLines(
            source=_source, bid=bid, idx=f"{idx:05}-00", lines=lines_of_page
        )
        yield page


def write_page_lines(
    pages: Iterator[PageLines], path_out: Path, overwrite: bool
) -> int:
    """Write the `PageLines` to file with a default file name.

    Args:
        pages (Iterator[PageLines]): The PageLines to write to disk.
        path_out (Path): The directory to write the PageLines to.
        overwrite (bool): Overwrite existing files if found.

    Returns:
        int: The count of the files written.
    """
    pages_list = list(pages)
    count = 0
    serializer = page_lines_serializer()
    for idx, page in enumerate(pages_list, start=1):
        result_path = path_out / page.default_file_name()
        serializer.save_as_json(
            path_out=result_path, complex_obj=page, overwrite=overwrite
        )
        count = idx
    return count
