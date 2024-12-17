"""Tests for next_local_time."""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from pbs_parse.snippets.datetime.next_local_time import is_before_raw, next_local_time

UTC = ZoneInfo("UTC")


def test_utc_ref_nieve_time_follows():
    """test_utc_ref_nieve_time_follows."""
    dt_ref = datetime(2024, 12, 16, 14, 30, tzinfo=UTC)
    delta = timedelta(days=1)
    next_time = time(15, 0, 0)
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time, delta=delta)
    assert next_dt == datetime(2024, 12, 16, 15, tzinfo=UTC)
    # check default timedelta conversion.
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time)
    assert next_dt == datetime(2024, 12, 16, 15, tzinfo=UTC)
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time, delta=timedelta(0))
    assert next_dt == datetime(2024, 12, 16, 15, tzinfo=UTC)
    # check less than one day conversion
    next_dt = next_local_time(
        dt_ref=dt_ref, next_time=next_time, delta=timedelta(hours=4)
    )
    assert next_dt == datetime(2024, 12, 16, 15, tzinfo=UTC)
    # check more than one day
    next_dt = next_local_time(
        dt_ref=dt_ref, next_time=next_time, delta=timedelta(days=1, hours=2)
    )
    assert next_dt == datetime(2024, 12, 17, 15, tzinfo=UTC)


def test_utc_ref_nieve_time_leads():
    """test_utc_ref_nieve_time_leads."""
    dt_ref = datetime(2024, 12, 16, 14, 30, tzinfo=UTC)
    delta = timedelta(days=1)
    next_time = time(12, 0, 0)
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time, delta=delta)
    assert next_dt == datetime(2024, 12, 17, 12, tzinfo=UTC)
    # check default timedelat conversion.
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time)
    assert next_dt == datetime(2024, 12, 17, 12, tzinfo=UTC)
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time, delta=timedelta(0))
    assert next_dt == datetime(2024, 12, 17, 12, tzinfo=UTC)
    # check less than one day conversion
    next_dt = next_local_time(
        dt_ref=dt_ref, next_time=next_time, delta=timedelta(hours=4)
    )
    assert next_dt == datetime(2024, 12, 17, 12, tzinfo=UTC)
    # check more than one day
    next_dt = next_local_time(
        dt_ref=dt_ref, next_time=next_time, delta=timedelta(days=1, hours=2)
    )
    assert next_dt == datetime(2024, 12, 18, 12, tzinfo=UTC)


def test_utc_ref_aware_time_follows():
    """test_utc_ref_aware_time_follows."""
    dt_ref = datetime(2024, 12, 16, 14, 30, tzinfo=UTC)
    delta = timedelta(days=1)
    tzinfo = ZoneInfo("America/Phoenix")
    next_time = time(15, 0, 0, tzinfo=tzinfo)
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time, delta=delta)
    assert next_dt == datetime(2024, 12, 16, 15, tzinfo=tzinfo)
    # check default timedelta conversion.
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time)
    assert next_dt == datetime(2024, 12, 16, 15, tzinfo=tzinfo)
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time, delta=timedelta(0))
    assert next_dt == datetime(2024, 12, 16, 15, tzinfo=tzinfo)
    # check less than one day conversion
    next_dt = next_local_time(
        dt_ref=dt_ref, next_time=next_time, delta=timedelta(hours=4)
    )
    assert next_dt == datetime(2024, 12, 16, 15, tzinfo=tzinfo)
    # check more than one day
    next_dt = next_local_time(
        dt_ref=dt_ref, next_time=next_time, delta=timedelta(days=1, hours=2)
    )
    assert next_dt == datetime(2024, 12, 17, 15, tzinfo=tzinfo)


def test_utc_ref_aware_time_leads():
    """test_utc_ref_aware_time_leads."""
    dt_ref = datetime(2024, 12, 16, 14, 30, tzinfo=UTC)
    delta = timedelta(days=1)
    tzinfo = ZoneInfo("America/Phoenix")
    next_time = time(12, 0, 0, tzinfo=tzinfo)
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time, delta=delta)
    assert next_dt == datetime(2024, 12, 17, 12, tzinfo=tzinfo)
    # check default timedelat conversion.
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time)
    assert next_dt == datetime(2024, 12, 17, 12, tzinfo=tzinfo)
    next_dt = next_local_time(dt_ref=dt_ref, next_time=next_time, delta=timedelta(0))
    assert next_dt == datetime(2024, 12, 17, 12, tzinfo=tzinfo)
    # check less than one day conversion
    next_dt = next_local_time(
        dt_ref=dt_ref, next_time=next_time, delta=timedelta(hours=4)
    )
    assert next_dt == datetime(2024, 12, 17, 12, tzinfo=tzinfo)
    # check more than one day
    next_dt = next_local_time(
        dt_ref=dt_ref, next_time=next_time, delta=timedelta(days=1, hours=2)
    )
    assert next_dt == datetime(2024, 12, 18, 12, tzinfo=tzinfo)


def test_is_before_raw():
    """test_is_before_raw ."""
    ref = time(15, 00)
    comp = time(13, 00)
    assert is_before_raw(ref_time=ref, comp_time=comp)
    ref = time(15, 00, tzinfo=UTC)
    comp = time(13, 00, tzinfo=ZoneInfo("America/Phoenix"))
    assert is_before_raw(ref_time=ref, comp_time=comp)
    ref = time(12, 00, tzinfo=UTC)
    comp = time(13, 00, tzinfo=ZoneInfo("America/Phoenix"))
    assert not is_before_raw(ref_time=ref, comp_time=comp)
