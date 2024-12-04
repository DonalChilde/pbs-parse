"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_TD
from pbs_parse.pbs_2022_01.parse import grammar
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar.page_header_2
result_class = grammar_TD.PageHeader2
test_name = "page_header_2" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="DP D/A EQ FLT#  STA DLCL/DHBT ML STA ALCL/AHBT  BLOCK  SYNTH   TPAY   DUTY  TAFB   FDP CALENDAR 05/02−06/01",
        result=grammar_TD.PageHeader2(
            from_date=grammar_TD.MonthDay(month="05", day="02"),
            to_date=grammar_TD.MonthDay(month="06", day="01"),
        ),
    )
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
