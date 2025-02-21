"""FILE: query.py."""

from collections.abc import Iterator

from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.page_lines import PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines
from pbs_parse.pbs_2022_01.pbs_store.store_manager import StoreManager


def page_lines(store: StoreManager, base_name: str) -> Iterator[PageLines]:
    """All PageLines in a base.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_

    Yields:
        Iterator[PageLines]: _description_
    """
    base = store.get_base(base_name=base_name)
    for file_info in base.pages.values():
        path_in = store.manifest_directory / file_info.file_path
        yield API.load.page_lines(file_in=path_in)


def trip_lines(store: StoreManager, base_name: str) -> Iterator[TripLines]:
    """all_trip_lines.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_

    Yields:
        Iterator[TripLines]: _description_
    """
    base = store.get_base(base_name=base_name)
    for file_info in base.raw_trips.values():
        path_in = store.manifest_directory / file_info.file_path
        yield API.load.trip_lines(file_in=path_in)


def parsed_trips(store: StoreManager, base_name: str) -> Iterator[ParsedTrip]:
    """all_parsed_trips.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_

    Yields:
        Iterator[ParsedTrip]: _description_
    """
    base = store.get_base(base_name=base_name)
    for file_info in base.parsed_trips.values():
        path_in = store.manifest_directory / file_info.file_path
        yield API.load.parsed_trip(file_in=path_in)


def expanded_trips(
    store: StoreManager, base_name: str, equipment: str = "_all_"
) -> Iterator[ExpandedTrip]:
    """expanded_trips.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_
        equipment (str, optional): _description_. Defaults to "_all_".

    Yields:
        Iterator[ExpandedTrip]: _description_
    """
    base = store.get_base(base_name=base_name)
    for file_info in base.expanded_trips.values():
        path_in = store.manifest_directory / file_info.file_path
        yield API.load.expanded_trip(file_in=path_in)


def expanded_trip_errors(store: StoreManager, base_name: str) -> dict[str, list[str]]:
    """Get the dict of all errors for expanded trips.

    returns an empty dict if no errors found.
    """
    base = store.get_base(base_name=base_name)
    # TODO eval wht this function promises. fail on bad key or no details?
    return base.details.expanded_errors
