"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_td
from pbs_parse.pbs_2022_01.parse import grammar
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar.trip_footer
result_class = grammar_td.TripFooter
test_name = "trip_footer" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="TTL                                              7.50   0.00   7.50        10.20       −− −− −−",
        result=result_class(
            block="7.50",
            synth="0.00",
            total_pay="7.50",
            tafb="10.20",
            calendar_entries=["−−", "−−", "−−"],
        ),
    ),
    ParsingTest[result_class](
        txt="TTL                                              7.50   0.00   7.50        10.20       ",
        result=result_class(
            block="7.50",
            synth="0.00",
            total_pay="7.50",
            tafb="10.20",
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
