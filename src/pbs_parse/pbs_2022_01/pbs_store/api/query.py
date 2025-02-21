"""FILE: query.py."""

from collections.abc import Iterator

from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.manifest import FileTypes
from pbs_parse.pbs_2022_01.models.page_lines import PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines
from pbs_parse.pbs_2022_01.pbs_store.store_manager import StoreManager

from . import load


def page_lines(store: StoreManager, base: str) -> Iterator[PageLines]:
    """All PageLines in a base.

    Args:
        store (StoreManager): _description_
        base (str): _description_

    Yields:
        Iterator[PageLines]: _description_
    """
    page_infos = store.get_file_info_by_type(base=base, file_type=FileTypes.SPLIT_PAGE)
    for page_info in page_infos:
        yield load.page_lines(store=store, base=base, key=page_info["key"])


def trip_lines(store: StoreManager, base: str) -> Iterator[TripLines]:
    """all_trip_lines.

    Args:
        store (StoreManager): _description_
        base (str): _description_

    Yields:
        Iterator[TripLines]: _description_
    """
    trip_infos = store.get_file_info_by_type(base=base, file_type=FileTypes.SPLIT_TRIP)
    for page_info in trip_infos:
        yield load.trip_lines(store=store, base=base, key=page_info["key"])


def parsed_trips(store: StoreManager, base: str) -> Iterator[ParsedTrip]:
    """all_parsed_trips.

    Args:
        store (StoreManager): _description_
        base (str): _description_

    Yields:
        Iterator[ParsedTrip]: _description_
    """
    trip_infos = store.get_file_info_by_type(base=base, file_type=FileTypes.PARSED_TRIP)
    for page_info in trip_infos:
        yield load.parsed_trip(store=store, base=base, key=page_info["key"])


def expanded_trips(
    store: StoreManager, base: str, equipment: str = "_all_"
) -> Iterator[ExpandedTrip]:
    """expanded_trips.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        equipment (str, optional): _description_. Defaults to "_all_".

    Yields:
        Iterator[ExpandedTrip]: _description_
    """
    trip_infos = store.get_file_info_by_type(
        base=base, file_type=FileTypes.EXPANDED_TRIP
    )
    for page_info in trip_infos:
        yield load.expanded_trip(store=store, base=base, key=page_info["key"])


def expanded_trip_errors(store: StoreManager, base: str) -> dict[str, list[str]]:
    """Get the dict of all errors for expanded trips.

    returns an empty dict if no errors found.
    """
    errors = store.manifest["bases"][base]["errors"].get(FileTypes.EXPANDED_TRIP, None)
    if errors is None:
        return {}
    return errors
