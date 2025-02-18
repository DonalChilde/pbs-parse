"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_td
from pbs_parse.pbs_2022_01.parse import grammar
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar.dutyperiod_report
result_class = grammar_td.DutyperiodReport
test_name = "duty_period_report" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="                RPT 1237/1237                                                           2 −− −− −− −− −− −−",
        result=result_class(
            report=grammar_td.DualTime(lcl="1237", hbt="1237"),
            calendar_entries=["2", "−−", "−−", "−−", "−−", "−−", "−−"],
        ),
    ),
    ParsingTest[result_class](
        txt="                RPT 1000/1000                                                          sequence 25384/30DEC",
        result=result_class(
            report=grammar_td.DualTime(lcl="1000", hbt="1000"), calendar_entries=[]
        ),
    ),
    ParsingTest[result_class](
        txt="                RPT 1829/1829                                                          sequence 01JUL",
        result=result_class(
            report=grammar_td.DualTime(lcl="1829", hbt="1829"), calendar_entries=[]
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
