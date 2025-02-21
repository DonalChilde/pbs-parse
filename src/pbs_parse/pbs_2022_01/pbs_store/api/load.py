"""FILE: load.py."""

import logging

from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.manifest import FileTypes
from pbs_parse.pbs_2022_01.models.page_lines import PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines
from pbs_parse.pbs_2022_01.pbs_store.exceptions import UnableToLoadError
from pbs_parse.pbs_2022_01.pbs_store.store_manager import StoreManager

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
        value = PageLines.model_validate(data)
        return value
    except Exception as e:
        msg = (
            f"Tried to make PageLines from json, but there was an error. "
            f"error={(e,)} {store=}, {base=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e


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
        value = TripLines.model_validate(data)
        return value
    except Exception as e:
        msg = (
            f"Tried to make TripLines from json, but there was an error. "
            f"error={(e,)} {store=}, {base=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e


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
        value = ParsedTrip.model_validate(data)
        return value
    except Exception as e:
        msg = (
            f"Tried to make ParsedTrip from json, but there was an error. "
            f"error={(e,)} {store=}, {base=}, {key=}"
        )
        logger.exception(msg)
        raise UnableToLoadError(msg) from e


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
        value = ExpandedTrip.model_validate(data)
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
