"""FILE: next_utc.py."""

from datetime import datetime, time, timedelta
from typing import Any

DELTA_ZERO = timedelta(seconds=0)


def next_utc(
    utc_datetime: datetime,
    delta: timedelta = DELTA_ZERO,
    next_time: time | None = None,
    over_24: timedelta = DELTA_ZERO,
    context: dict[str, Any] | None = None,
) -> datetime:
    """next_utc.

    Args:
        utc_datetime (datetime): _description_
        delta (timedelta, optional): _description_. Defaults to DELTA_ZERO.
        next_time (time | None, optional): _description_. Defaults to None.
        over_24 (timedelta, optional): _description_. Defaults to DELTA_ZERO.
        context (dict[str, Any] | None, optional): _description_. Defaults to None.

    Returns:
        datetime: _description_
    """
    return next_utc_from_timedelta(utc_datetime=utc_datetime, delta=delta)


def next_utc_from_timedelta(utc_datetime: datetime, delta: timedelta) -> datetime:
    """next_utc_from_timedelta.

    Args:
        utc_datetime (datetime): _description_
        delta (timedelta): _description_

    Returns:
        datetime: _description_
    """
    next_utc = utc_datetime + delta
    return next_utc


def next_utc_from_local_time() -> datetime:
    """next_utc_from_local_time.

    Returns:
        datetime: _description_
    """
    pass
