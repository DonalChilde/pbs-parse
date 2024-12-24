"""Extract trip lines from page lines."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from pfmsoft.indexed_string.model import IndexedString

from pbs_parse.pbs_2022_01.models.page_lines import PAGE_LINES_SERIALIZER, PageLines
from pbs_parse.pbs_2022_01.models.trip_lines import TRIP_LINES_SERIALIZER, TripLines


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
        if indexed_line.txt.startswith("TTL"):
            result = accumulated_lines
            accumulated_lines = []
            is_trip = False
            yield result


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
    """Split the TripLines from a PageLines.

    Args:
        page (PageLines): The PageLines.

    Yields:
        Iterator[TripLines]: The TripLines.
    """
    for idx, trip_lines in enumerate(
        lines_of_page_to_lines_of_trips(page.lines), start=1
    ):
        trip = TripLines(
            source=page.uuid,
            idx=idx,
            page_idx=page.idx,
            lines=[page.lines[0], page.lines[1], *trip_lines, page.lines[-1]],
        )
        yield trip


def write_trip_lines(
    file_stem: str, trips: Iterator[TripLines], path_out: Path, overwrite: bool
):
    """Write TripLines to a file.

    Args:
        file_stem (str): The first part of the output file name, usually the stem of
            the PageLines input file.
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
