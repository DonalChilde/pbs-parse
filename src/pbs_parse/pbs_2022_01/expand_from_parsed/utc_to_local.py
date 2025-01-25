"""FILE: utc_to_local.py."""

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


def utc_to_local(utc: datetime, local_tz: ZoneInfo, ref: str) -> datetime:
    """utc_to_local.

    This is to try and track down dst fold errors.

    Args:
        utc (datetime): _description_
        local_tz (ZoneInfo): _description_
        ref (str): _description_

    Returns:
        datetime: _description_
    """
    local = utc.astimezone(local_tz)
    if local.strftime("%H%M") != ref:
        logger.warning(f"{utc=!r} to {local=!r} does not match {ref=!r}")
    return local
