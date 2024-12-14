"""Test round tripping aware datetimes.

tzname() returns uncertain values, eg America/Phoenix -> MST
"""

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from pbs_parse.snippets.datetime.iso8601_datetime import (
    AwareDatetimeIsoTD,
    deserialize_dt,
    serialize_dt,
)

logger = logging.getLogger(__name__)


def test_datetime_roundtrip_basic():
    """Test round trip with basic objects."""
    dt = datetime.now(ZoneInfo("America/Phoenix"))
    serialized = AwareDatetimeIsoTD(iso_format=dt.isoformat(), tz_name=dt.tzname())
    dt_from_iso = datetime.fromisoformat(serialized["iso_format"])
    assert dt == dt_from_iso
    assert dt.tzinfo != dt_from_iso.tzinfo
    dt_from_iso_with_tz = dt_from_iso.astimezone(ZoneInfo(serialized["tz_name"]))  # type: ignore
    assert dt_from_iso_with_tz == dt


def test_roundtrip_datetime():
    """test_roundtrip_datetime."""
    dt = datetime.now(ZoneInfo("America/Phoenix"))
    logger.info(f"dt: {dt!r}")
    serialized = serialize_dt(value=dt)

    logger.info(f"serialized: {serialized}")
    assert serialized == AwareDatetimeIsoTD(
        iso_format=dt.isoformat(), tz_name=dt.tzname()
    )
    deserialized = deserialize_dt(value=serialized)
    logger.info(f"{deserialized!r}")

    assert deserialized == dt
    assert deserialized.tzinfo != dt.tzinfo
