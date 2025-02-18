"""Adapted types for use with pydantic."""

from typing import Annotated

from pydantic import (
    BeforeValidator,
    PlainSerializer,
)
from whenever import Date, TimeDelta, ZonedDateTime


def date_validator(v: str | Date) -> Date:
    """Validate whenever.Date."""
    if isinstance(v, Date):
        return v

    return Date.parse_common_iso(v)


PydanticDate = Annotated[
    Date,
    BeforeValidator(date_validator),
    PlainSerializer(lambda x: x.format_common_iso()),
]


def zoned_validator(v: str | ZonedDateTime) -> ZonedDateTime:
    """Validate whenever.ZonedDateTime."""
    if isinstance(v, ZonedDateTime):
        return v
    return ZonedDateTime.parse_common_iso(v)


PydanticZonedDateTime = Annotated[
    ZonedDateTime,
    BeforeValidator(zoned_validator),
    PlainSerializer(lambda x: x.format_common_iso()),
]


def timedelta_validator(v: str | TimeDelta) -> TimeDelta:
    """Validate whenever.TimeDelta."""
    if isinstance(v, TimeDelta):
        return v
    return TimeDelta.parse_common_iso(v)


PydanticTimeDelta = Annotated[
    TimeDelta,
    BeforeValidator(timedelta_validator),
    PlainSerializer(lambda x: x.format_common_iso()),
]
