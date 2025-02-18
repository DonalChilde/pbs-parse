"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_td
from pbs_parse.pbs_2022_01.parse import grammar
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar.flight
result_class = grammar_td.Flight
test_name = "flight" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="1  1/1 65 2131  SAN 1337/1337    ORD 1935/1735   3.58          1.10X                   −− −− −− −− −− −− −−",
        result=result_class(
            dutyperiod_idx="1",
            depart_day="1",
            arrive_day="1",
            equipment_code="65",
            flight_number="2131",
            deadhead=False,
            deadhead_code="",
            departure_station="SAN",
            departure_time=grammar_td.DualTime(lcl="1337", hbt="1337"),
            crew_meal="",
            arrival_station="ORD",
            arrival_time=grammar_td.DualTime(lcl="1935", hbt="1735"),
            block="3.58",
            synth="0.00",
            ground="1.10",
            equipment_change=True,
            calendar_entries=["−−", "−−", "−−", "−−", "−−", "−−", "−−"],
        ),
    ),
]


def idfn(val: ParsingTest[result_class]) -> str:
    """Return a custom test name for parameterized tests."""
    return test_name


@pytest.mark.parametrize("test_data", test_items, ids=idfn)
def test_grammar(test_data: ParsingTest[result_class]):
    """Parse a string and test against expected result."""
    parse_result = parser.parse_string(test_data.txt)
    logger.info(f"Text: {test_data.txt!r}")
    logger.info(f"Expected: {test_data.result!r}")
    logger.info(f"Received: {parse_result.dump()}")
    assert parse_result[0] == test_data.result
