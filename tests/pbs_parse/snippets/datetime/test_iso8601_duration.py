"""Tests for iso8601 duration."""

import logging
from datetime import timedelta

from pbs_parse.snippets.datetime import iso8601_duration as ID

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_string_to_dict():
    """Test parsing to dict."""
    dur_1 = "P1Y2.3MT2H"
    result_1 = ID.string_to_dict(dur=dur_1)
    assert result_1 == {
        "sign": "",
        "years": "1",
        "months": "2.3",
        "weeks": "0",
        "days": "0",
        "separator": "T",
        "hours": "2",
        "minutes": "0",
        "seconds": "0",
    }


def test_to_from_iso8601():
    """Round trip timedeltas."""
    td = timedelta(days=3, hours=2, seconds=4, microseconds=34)
    td_iso = ID.timedelta_to_isoformat(td=td)
    td_from_string = ID.string_to_timedelta(dur=td_iso)
    logger.info(f"{td}, {td_iso}, {td_from_string}")
    assert td == td_from_string

    td = timedelta(0) - timedelta(days=3, hours=2, seconds=4, microseconds=34)
    td_iso = ID.timedelta_to_isoformat(td=td)
    td_from_string = ID.string_to_timedelta(dur=td_iso)
    logger.info(f"{td}, {td_iso}, {td_from_string}")
    assert td == td_from_string

    td = timedelta(days=3)
    td_iso = ID.timedelta_to_isoformat(td=td)
    td_from_string = ID.string_to_timedelta(dur=td_iso)
    logger.info(f"{td}, {td_iso}, {td_from_string}")
    assert td == td_from_string

    td = timedelta(hours=2, seconds=4, microseconds=34)
    td_iso = ID.timedelta_to_isoformat(td=td)
    td_from_string = ID.string_to_timedelta(dur=td_iso)
    logger.info(f"{td}, {td_iso}, {td_from_string}")
    assert td == td_from_string

    td = timedelta(days=3, microseconds=34)
    td_iso = ID.timedelta_to_isoformat(td=td)
    td_from_string = ID.string_to_timedelta(dur=td_iso)
    logger.info(f"{td}, {td_iso}, {td_from_string}")
    assert td == td_from_string

    td = timedelta(0)
    td_iso = ID.timedelta_to_isoformat(td=td)
    td_from_string = ID.string_to_timedelta(dur=td_iso)
    logger.info(f"{td}, {td_iso}, {td_from_string}")
    assert td == td_from_string
