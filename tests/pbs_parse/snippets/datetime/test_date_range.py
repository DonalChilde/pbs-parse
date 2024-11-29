"""Tests for date_range."""

# ruff: noqa: D103
import logging
from datetime import date, datetime

from pbs_parse.snippets.datetime.date_range import date_range

logger = logging.getLogger(__name__)


def test_forward_inclusive():
    start = date(2024, 10, 1)
    end = date(2024, 10, 5)
    dates = list(date_range(start, end))
    # logger.info(f"{locals()}")
    assert len(dates) == 5
    assert dates[0] == start
    assert dates[-1] == end


def test_forward_not_inclusive():
    start = date(2024, 10, 1)
    end = date(2024, 10, 5)
    dates = list(date_range(start, end, inclusive=False))
    logger.info(f"{locals()}")
    assert len(dates) == 4
    assert dates[0] == date(2024, 10, 1)
    assert dates[-1] == date(2024, 10, 4)


def test_backward_inclusive():
    end = date(2024, 10, 1)
    start = date(2024, 10, 5)
    dates = list(date_range(start, end))
    logger.info(f"{locals()}")
    assert len(dates) == 5
    assert dates[-1] == date(2024, 10, 1)
    assert dates[0] == date(2024, 10, 5)


def test_backward_not_inclusive():
    end = date(2024, 10, 1)
    start = date(2024, 10, 5)
    dates = list(date_range(start, end, inclusive=False))
    print(f"{dates!r}")
    assert len(dates) == 4
    assert dates[-1] == date(2024, 10, 2)
    assert dates[0] == date(2024, 10, 5)


def test_same_dates():
    end = date(2024, 10, 1)
    start = date(2024, 10, 1)
    dates = list(date_range(start, end, inclusive=False))
    print(f"{dates!r}")
    assert len(dates) == 0
    dates = list(date_range(start, end, inclusive=True))
    assert len(dates) == 1
    assert dates[0] == start


def test_datetime():
    start = datetime(2024, 10, 1)
    end = datetime(2024, 10, 5)
    dates = list(date_range(start, end))
    assert len(dates) == 5
    assert dates[0] == date(2024, 10, 1)
    assert dates[-1] == date(2024, 10, 5)
