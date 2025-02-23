"""FILE: load.py."""

import logging
from collections.abc import Iterable

from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.page_lines import PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines
from pbs_parse.pbs_2022_01.pbs_store.exceptions import UnableToLoadError
from pbs_parse.pbs_2022_01.pbs_store.store_manager import StoreManager

logger = logging.getLogger(__name__)


def page(store: StoreManager, base_name: str, key: str) -> PageLines:
    """page_lines.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_
        key (str): _description_

    Raises:
        UnableToLoadError: _description_

    Returns:
        PageLines: _description_
    """
    try:
        path_in = store.get_page_path(base_name=base_name, key=key)
        value = API.load.page_lines(file_in=path_in)
        return value
    except Exception as e:
        msg = (
            f"Tried to make PageLines from json, but there was an error. "
            f"error={(e,)} {store=}, {base_name=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e


def all_pages(store: StoreManager, base_name: str) -> Iterable[PageLines]:
    """all_pages.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_

    Returns:
        Iterable[PageLines]: _description_

    Yields:
        Iterator[Iterable[PageLines]]: _description_
    """
    base = store.get_base(base_name=base_name)
    file_infos = base.pages
    for info in file_infos.values():
        yield page(store=store, base_name=base_name, key=info.key)


def all_raw_trips(store: StoreManager, base_name: str) -> Iterable[TripLines]:
    """all_raw_trips.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_

    Returns:
        Iterable[TripLines]: _description_

    Yields:
        Iterator[Iterable[TripLines]]: _description_
    """
    base = store.get_base(base_name=base_name)
    file_infos = base.raw_trips
    for info in file_infos.values():
        yield raw_trip(store=store, base_name=base_name, key=info.key)


def all_parsed_trips(store: StoreManager, base_name: str) -> Iterable[ParsedTrip]:
    """all_parsed_trips.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_

    Returns:
        Iterable[ParsedTrip]: _description_

    Yields:
        Iterator[Iterable[ParsedTrip]]: _description_
    """
    base = store.get_base(base_name=base_name)
    file_infos = base.parsed_trips
    for info in file_infos.values():
        yield parsed_trip(store=store, base_name=base_name, key=info.key)


def all_expanded_trips(store: StoreManager, base_name: str) -> Iterable[ExpandedTrip]:
    """all_expanded_trips.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_

    Returns:
        Iterable[ExpandedTrip]: _description_

    Yields:
        Iterator[Iterable[ExpandedTrip]]: _description_
    """
    base = store.get_base(base_name=base_name)
    file_infos = base.expanded_trips
    for info in file_infos.values():
        yield expanded_trip(store=store, base_name=base_name, key=info.key)


def all_expanded_trips_with_errors(
    store: StoreManager, base_name: str
) -> Iterable[ExpandedTrip]:
    """all_expanded_trips_with_errors.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_

    Returns:
        Iterable[ExpandedTrip]: _description_

    Yields:
        Iterator[Iterable[ExpandedTrip]]: _description_
    """
    base = store.get_base(base_name=base_name)
    error_keys = base.expanded_trips_with_errors
    for key in error_keys:
        yield expanded_trip(store=store, base_name=base_name, key=key)


def raw_trip(store: StoreManager, base_name: str, key: str) -> TripLines:
    """trip_lines.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_
        key (str): _description_

    Raises:
        UnableToLoadError: _description_

    Returns:
        TripLines: _description_
    """
    try:
        path_in = store.get_raw_trip_path(base_name=base_name, key=key)
        value = API.load.trip_lines(file_in=path_in)
        return value
    except Exception as e:
        msg = (
            f"Tried to make TripLines from json, but there was an error. "
            f"error={(e,)} {store=}, {base_name=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e


def parsed_trip(store: StoreManager, base_name: str, key: str) -> ParsedTrip:
    """parsed_trip.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_
        key (str): _description_

    Raises:
        UnableToLoadError: _description_

    Returns:
        ParsedTrip: _description_
    """
    try:
        path_in = store.get_parsed_trip_path(base_name=base_name, key=key)
        value = API.load.parsed_trip(file_in=path_in)
        return value
    except Exception as e:
        msg = (
            f"Tried to make ParsedTrip from json, but there was an error. "
            f"error={(e,)} {store=}, {base_name=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e


def expanded_trip(store: StoreManager, base_name: str, key: str) -> ExpandedTrip:
    """expanded_trip.

    Args:
        store (StoreManager): _description_
        base_name (str): _description_
        key (str): _description_

    Raises:
        UnableToLoadError: _description_

    Returns:
        ExpandedTrip: _description_
    """
    try:
        path_in = store.get_expanded_trip_path(base_name=base_name, key=key)
        value = API.load.expanded_trip(file_in=path_in)
        return value
    except Exception as e:
        msg = (
            f"Tried to make ExpandedTrip from json, but there was an error. "
            f"error={(e,)} {store=}, {base_name=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e
