"""FILE: next_local_time_in_utc.py."""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

UTC = ZoneInfo("UTC")


def next_local_time_in_utc(
    utc_start: datetime, next_lcl: time, next_tz_name: str
) -> datetime:
    """Calculate the next occurance of a time in UTC.

    Calulate the next occurance of a datetime in UTC when only the
    following information is know.

    This does not handle times `in the fold` of DST. eg november fall back.

    Args:
        utc_start (datetime): The datetime in UTC to reference
        next_lcl (time): The local `time` that falls after `utc_start`
        next_tz_name (str): The timezone name of `next_nieve`.

    Returns:
        datetime: The next datetime in UTC
    """
    local_tz = ZoneInfo(next_tz_name)
    next_datetime = datetime.combine(
        date=utc_start.astimezone(local_tz).date(),
        time=next_lcl,
        tzinfo=local_tz,
    )
    if next_datetime < utc_start.astimezone(local_tz):
        # increment utc_start if `next_datetime` comes before a localized utc_start.
        utc_start_increment = utc_start + timedelta(days=1)
        next_datetime = datetime.combine(
            date=utc_start_increment.astimezone(local_tz).date(),
            time=next_lcl,
            tzinfo=local_tz,
        )
    return next_datetime.astimezone(UTC)
