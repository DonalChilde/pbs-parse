"""FILE: load.py."""

import logging
from collections.abc import Iterator

from pbs_parse.pbs_2022_01.models.expanded import EXPANDED_TRIP_SERIALIZER, ExpandedTrip
from pbs_parse.pbs_2022_01.models.manifest import FileTypes
from pbs_parse.pbs_2022_01.models.page_lines import PAGE_LINES_SERIALIZER, PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER, ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TRIP_LINES_SERIALIZER, TripLines
from pbs_parse.pbs_2022_01.pbs_manifest.exceptions import UnableToLoadError
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

logger = logging.getLogger(__name__)


def page_lines(store: StoreManager, base: str, key: str) -> PageLines:
    """page_lines.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        key (str): _description_

    Raises:
        UnableToLoadError: _description_

    Returns:
        PageLines: _description_
    """
    data = store.load_resource(base=base, key=key)
    try:
        value = PAGE_LINES_SERIALIZER.from_simple(data)  # type: ignore
        return value
    except Exception as e:
        msg = (
            f"Tried to make PageLines from json, but there was an error. "
            f"error={(e,)} {store=}, {base=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e


def all_page_lines(store: StoreManager, base: str) -> Iterator[PageLines]:
    """all_page_lines.

    Args:
        store (StoreManager): _description_
        base (str): _description_

    Yields:
        Iterator[PageLines]: _description_
    """
    page_infos = store.get_file_info_by_type(base=base, file_type=FileTypes.SPLIT_PAGE)
    for page_info in page_infos:
        yield page_lines(store=store, base=base, key=page_info["key"])


def trip_lines(store: StoreManager, base: str, key: str) -> TripLines:
    """trip_lines.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        key (str): _description_

    Raises:
        UnableToLoadError: _description_

    Returns:
        TripLines: _description_
    """
    data = store.load_resource(base=base, key=key)
    try:
        value = TRIP_LINES_SERIALIZER.from_simple(data)  # type: ignore
        return value
    except Exception as e:
        msg = (
            f"Tried to make TripLines from json, but there was an error. "
            f"error={(e,)} {store=}, {base=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e


def all_trip_lines(store: StoreManager, base: str) -> Iterator[TripLines]:
    """all_trip_lines.

    Args:
        store (StoreManager): _description_
        base (str): _description_

    Yields:
        Iterator[TripLines]: _description_
    """
    trip_infos = store.get_file_info_by_type(base=base, file_type=FileTypes.SPLIT_TRIP)
    for page_info in trip_infos:
        yield trip_lines(store=store, base=base, key=page_info["key"])


def parsed_trip(store: StoreManager, base: str, key: str) -> ParsedTrip:
    """parsed_trip.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        key (str): _description_

    Raises:
        UnableToLoadError: _description_

    Returns:
        ParsedTrip: _description_
    """
    data = store.load_resource(base=base, key=key)
    try:
        logger.info(data)
        value = PARSED_TRIP_SERIALIZER.from_simple(data)  # type: ignore
        return value
    except Exception as e:
        msg = (
            f"Tried to make ParsedTrip from json, but there was an error. "
            f"error={(e,)} {store=}, {base=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e


def all_parsed_trips(store: StoreManager, base: str) -> Iterator[ParsedTrip]:
    """all_parsed_trips.

    Args:
        store (StoreManager): _description_
        base (str): _description_

    Yields:
        Iterator[ParsedTrip]: _description_
    """
    trip_infos = store.get_file_info_by_type(base=base, file_type=FileTypes.PARSED_TRIP)
    for page_info in trip_infos:
        yield parsed_trip(store=store, base=base, key=page_info["key"])


def expanded_trip(store: StoreManager, base: str, key: str) -> ExpandedTrip:
    """expanded_trip.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        key (str): _description_

    Raises:
        UnableToLoadError: _description_

    Returns:
        ExpandedTrip: _description_
    """
    data = store.load_resource(base=base, key=key)
    try:
        value = EXPANDED_TRIP_SERIALIZER.from_simple(data)  # type: ignore
        return value
    except Exception as e:
        msg = (
            f"Tried to make ExpandedTrip from json, but there was an error. "
            f"error={(e,)} {store=}, {base=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e


def expanded_trip_errors(store: StoreManager, base: str, key: str) -> list[str]:
    """Get the list of errors for an expanded trip.

    returns an empty list if no errors found.
    """
    errors = store.manifest["bases"][base]["errors"].get(FileTypes.EXPANDED_TRIP, None)
    if errors is None:
        return []
    errors = store.manifest["bases"][base]["errors"][FileTypes.EXPANDED_TRIP].get(
        key, []
    )
    return errors


def all_expanded_trips(store: StoreManager, base: str) -> Iterator[ExpandedTrip]:
    """all_expanded_trips.

    Args:
        store (StoreManager): _description_
        base (str): _description_

    Yields:
        Iterator[ExpandedTrip]: _description_
    """
    trip_infos = store.get_file_info_by_type(
        base=base, file_type=FileTypes.EXPANDED_TRIP
    )
    for page_info in trip_infos:
        yield expanded_trip(store=store, base=base, key=page_info["key"])


def all_expanded_trip_errors(store: StoreManager, base: str) -> dict[str, list[str]]:
    """Get the dict of all errors for expanded trips.

    returns an empty dict if no errors found.
    """
    errors = store.manifest["bases"][base]["errors"].get(FileTypes.EXPANDED_TRIP, None)
    if errors is None:
        return {}
    return errors
