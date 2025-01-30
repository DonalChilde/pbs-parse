"""FILE: next_utc.py."""

from typing import Any

from whenever import Time, TimeDelta, ZonedDateTime

DELTA_ZERO = TimeDelta(seconds=0)


def next_utc(
    zoned_datetime: ZonedDateTime,
    delta: TimeDelta = DELTA_ZERO,
    next_time: Time | None = None,
    over_24: TimeDelta = DELTA_ZERO,
    context: dict[str, Any] | None = None,
) -> ZonedDateTime:
    """next_utc.

    Args:
        zoned_datetime (ZonedDateTime): _description_
        delta (TimeDelta, optional): _description_. Defaults to DELTA_ZERO.
        next_time (Time | None, optional): _description_. Defaults to None.
        over_24 (TimeDelta, optional): _description_. Defaults to DELTA_ZERO.
        context (dict[str, Any] | None, optional): _description_. Defaults to None.

    Returns:
        ZonedDateTime: _description_
    """
    return next_utc_from_timedelta(utc_datetime=zoned_datetime, delta=delta)


def next_utc_from_timedelta(
    utc_datetime: ZonedDateTime, delta: TimeDelta
) -> ZonedDateTime:
    """next_utc_from_timedelta.

    Args:
        utc_datetime (datetime): _description_
        delta (timedelta): _description_

    Returns:
        datetime: _description_
    """
    next_utc = utc_datetime + delta
    return next_utc


def next_utc_from_local_time() -> ZonedDateTime:
    """next_utc_from_local_time.

    Returns:
        datetime: _description_
    """
    pass
