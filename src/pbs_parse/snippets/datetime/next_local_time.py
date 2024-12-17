"""next_local_time."""

from datetime import date, datetime, time, timedelta
from math import ceil


def next_local_time(
    dt_ref: datetime, next_time: time, delta: timedelta | None = None
) -> datetime:
    """Calculate the full datetime of the next occurance of a time after a reference datetime.

    Calulate the next occurance of a datetime in UTC when only the
    following information is known.

    This does not handle times `in the fold` of DST. eg november fall back.

    Args:
        dt_ref (datetime): The reference datetime. Must be aware datetime.
        next_time (time): The `time` that falls after `dt_ref`. If the time has no
            tzinfo, it is assumed to be the same as the dt_ref.
        delta (timedelta | None): Used if the next_time is more than one day ahead.
            1 day or less means that the next_time falls within the next 24 hours.
            More than one day signals that the time is within the 24 hour period ending
            (math.ceil(delta/timedelta(days=1)) days ahead.


    Returns:
        datetime: The next datetime in the same tz as the dt_ref.
    """
    if delta is None or delta == timedelta(seconds=0):
        delta = timedelta(hours=24)
    abs_delta = abs(delta)
    days = abs_delta / timedelta(days=1)
    days = ceil(days)
    if dt_ref.tzinfo is None:
        raise ValueError("dt_ref must be an aware datetime.")
    if next_time.tzinfo is None:
        next_tzinfo = dt_ref.tzinfo
    else:
        next_tzinfo = next_time.tzinfo
    # if the raw next_time is before the raw dt_ref time, advance the day window.
    if is_before_raw(ref_time=dt_ref.time(), comp_time=next_time):
        days = days + 1

    localized_dt_ref_ordinal = dt_ref.astimezone(next_tzinfo).date().toordinal()
    next_ordinal = localized_dt_ref_ordinal + days - 1
    next_date = date.fromordinal(next_ordinal)

    next_datetime = datetime.combine(
        date=next_date,
        time=next_time,
        tzinfo=next_tzinfo,
    )
    # check to see if the next_time was less than the dt_ref time.
    if next_datetime < dt_ref.astimezone(next_tzinfo):
        next_ordinal = next_datetime.date().toordinal() + 1
        next_datetime = datetime.combine(
            date=date.fromordinal(next_ordinal),
            time=next_time,
            tzinfo=next_tzinfo,
        )
    return next_datetime


def is_before_raw(ref_time: time, comp_time: time) -> bool:
    raw_ref = time.fromisoformat(ref_time.strftime("%H%M%S.%f"))
    raw_comp = time.fromisoformat(comp_time.strftime("%H%M%S.%f"))
    return raw_comp < raw_ref
