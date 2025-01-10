"""FILE: load.py."""

import logging

from pbs_parse.pbs_2022_01.models.expanded_validation import (
    EXPANDED_VALIDATION_SERIALIZER,
    ExpandedValidation,
)
from pbs_parse.pbs_2022_01.pbs_manifest.exceptions import UnableToLoadError
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

logger = logging.getLogger(__name__)


def expanded_trip_validation(
    store: StoreManager, base: str, uuid: str
) -> ExpandedValidation:
    """expanded_trip_validation.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        uuid (str): _description_

    Raises:
        UnableToLoadError: _description_

    Returns:
        ExpandedValidation: _description_
    """
    data = store.load_resource(base=base, uuid=uuid)
    try:
        value = EXPANDED_VALIDATION_SERIALIZER.from_simple(data)  # type: ignore
        return value
    except Exception as e:
        msg = f"Tried to make ExpandedValidation from json, but there was an error. {base=}, {uuid=}"
        logger.exception(msg)
        raise UnableToLoadError(msg) from e
