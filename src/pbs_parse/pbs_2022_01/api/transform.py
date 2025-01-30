"""FILE: transform.py."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from pfmsoft.state_parser import ParseContext

from pbs_parse.pbs_2022_01.expand_from_parsed.parsed_to_expanded import ParsedToExpanded
from pbs_parse.pbs_2022_01.models.bid_data import BidData
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.page_lines import PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines
from pbs_parse.pbs_2022_01.parse.trip_lines_parser import parse_trip
from pbs_parse.pbs_2022_01.split.extract_pages import parse_page_lines_from_file
from pbs_parse.pbs_2022_01.split.extract_trips import parse_trip_lines

from . import save


def source_to_pages(path_in: Path, bid: BidData) -> Iterator[PageLines]:
    """source_to_pages.

    Args:
        path_in (Path): _description_
        bid (BidData): _description_

    Yields:
        Iterator[PageLines]: _description_
    """
    yield from parse_page_lines_from_file(path_in=path_in, bid=bid)


def pages_to_trips(pages: Iterable[PageLines]) -> Iterator[TripLines]:
    """pages_to_trips.

    Args:
        pages (Iterable[PageLines]): _description_

    Yields:
        Iterator[TripLines]: _description_
    """
    for page in pages:
        yield from parse_trip_lines(page=page)


def trips_to_parsed(trips: Iterable[TripLines]) -> Iterator[ParsedTrip]:
    """trips_to_parsed.

    Args:
        trips (Iterable[TripLines]): _description_

    Yields:
        Iterator[ParsedTrip]: _description_
    """
    for trip in trips:
        ctx = ParseContext()
        yield parse_trip(ctx=ctx, trip=trip)


def parsed_to_expanded(
    parsed_trips: Iterable[ParsedTrip], debug_dir: Path | None = None
) -> Iterator[ExpandedTrip]:
    """parsed_to_expanded.

    Args:
        parsed_trips (Iterable[ParsedTrip]): _description_
        debug_dir (Path | None, optional): _description_. Defaults to None.

    Yields:
        Iterator[ExpandedTrip]: _description_
    """
    for parsed in parsed_trips:
        parser = ParsedToExpanded(parsed_trip=parsed)
        expanded_trips = parser.translate()
        for expanded in expanded_trips:
            if expanded.errors and debug_dir is not None:
                save.expanded_debug(dir_out=debug_dir, parsed=parsed, expanded=expanded)
            yield expanded
