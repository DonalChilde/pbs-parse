"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_TD
from pbs_parse.pbs_2022_01.parse import grammar
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar.dutyperiod_release
result_class = grammar_TD.DutyPeriodRelease
test_name = "dutyperiod_release" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="                                 RLS 0739/0439   4.49   0.00   4.49   6.19        5.49 −− −− −− −− −− −− −−",
        result=result_class(
            release=grammar_TD.DualTime(lcl="0739", hbt="0439"),
            block="4.49",
            synth="0.00",
            total_pay="4.49",
            duty="6.19",
            flight_duty="5.49",
            calendar_entries=["−−", "−−", "−−", "−−", "−−", "−−", "−−"],
        ),
    ),
    ParsingTest[result_class](
        txt="                                 RLS 2252/2252   0.00   5.46   5.46   6.46        0.00",
        result=result_class(
            release=grammar_TD.DualTime(lcl="2252", hbt="2252"),
            block="0.00",
            synth="5.46",
            total_pay="5.46",
            duty="6.46",
            flight_duty="0.00",
            calendar_entries=[],
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
