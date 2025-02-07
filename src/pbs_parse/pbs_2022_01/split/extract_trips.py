"""Extract trip lines from page lines."""

from collections.abc import Iterable, Iterator
from copy import deepcopy
from pathlib import Path

from pfmsoft.indexed_string.model import IndexedString

from pbs_parse.pbs_2022_01.models.page_lines import PAGE_LINES_SERIALIZER, PageLines
from pbs_parse.pbs_2022_01.models.trip_lines import (
    TRIP_LINES_SERIALIZER,
    TripLines,
    TripLinesSource,
)


def lines_of_page_to_lines_of_trips(
    lines: Iterable[IndexedString],
) -> Iterator[list[IndexedString]]:
    """Extract the lines of a trip from the lines of a page.

    Args:
        lines (Iterable[IndexedString]): The lines of a page.

    Yields:
        Iterator[list[IndexedString]]: The lines of a trip.
    """
    is_trip = False
    accumulated_lines: list[IndexedString] = []
    for indexed_line in lines:
        if is_trip:
            accumulated_lines.append(indexed_line)
        else:
            if indexed_line.txt.startswith("SEQ"):
                is_trip = True
                accumulated_lines.append(indexed_line)
        if is_trip and indexed_line.txt.startswith("−−−"):
            accumulated_lines.pop()
            yield accumulated_lines
            accumulated_lines = list()
            is_trip = False


def parse_trip_lines_from_file(path_in: Path) -> Iterator[TripLines]:
    """Load a PageLines from file, and split to TripLines.

    Args:
        path_in (Path): Path to a PageLines.

    Yields:
        Iterator[TripLines]: The TripLines in a PageLines.
    """
    page = PAGE_LINES_SERIALIZER.load_from_json(path_in=path_in)
    yield from parse_trip_lines(page=page)


def parse_trip_lines(page: PageLines) -> Iterator[TripLines]:
    """parse_trip_lines.

    Args:
        page (PageLines): _description_

    Yields:
        Iterator[TripLines]: _description_
    """
    for idx, trip_lines in enumerate(
        lines_of_page_to_lines_of_trips(page.lines), start=1
    ):
        page_number = page.idx.split("-")[0]
        source = TripLinesSource(
            txt_file=page.source.txt_file, page_lines=page.default_file_name()
        )
        trip = TripLines(
            source=source,
            bid=deepcopy(page.bid),
            idx=f"{page_number}-{idx:02}",
            lines=[page.lines[0], page.lines[1], *trip_lines, page.lines[-1]],
        )
        yield trip


def write_trip_lines(trips: Iterator[TripLines], path_out: Path, overwrite: bool):
    """Write TripLines to a file.

    Args:
        trips (Iterator[TripLines]): The TripLines to write to disk.
        path_out (Path): The directory to write the TripLines to.
        overwrite (bool): Overwrite existing files if found.

    Returns:
        int: The count of the files written.
    """
    trips_list = list(trips)
    count = 0
    for idx, trip in enumerate(trips_list, start=1):
        result_path = path_out / trip.default_file_name()
        TRIP_LINES_SERIALIZER.save_as_json(
            path_out=result_path, complex_obj=trip, overwrite=overwrite
        )
        count = idx
    return count
