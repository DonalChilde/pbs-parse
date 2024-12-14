"""Models for use with datetimes."""

from datetime import datetime
from typing import TypedDict
from zoneinfo import ZoneInfo


class AwareDatetimeIsoTD(TypedDict):
    """Dict to hold datetime info."""

    iso_format: str
    tz_name: str | None


def deserialize_dt(value: AwareDatetimeIsoTD) -> datetime:
    """Deserialize datetime.

    Args:
        value (AwareDatetimeIsoTD): _description_

    Returns:
        datetime: _description_
    """
    dt = datetime.fromisoformat(value["iso_format"])
    if value["tz_name"] is not None:
        return dt.astimezone(ZoneInfo(value["tz_name"]))
    return dt


def serialize_dt(value: datetime) -> AwareDatetimeIsoTD:
    """Serialize datetime.

    Args:
        value (datetime): _description_

    Returns:
        AwareDatetimeIsoTD: _description_
    """
    return AwareDatetimeIsoTD(iso_format=value.isoformat(), tz_name=value.tzname())
