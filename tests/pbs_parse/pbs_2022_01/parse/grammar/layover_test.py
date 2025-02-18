"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_td
from pbs_parse.pbs_2022_01.parse import grammar
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar.layover
result_class = grammar_td.Layover
test_name = "layover" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="                MIA SONESTA MIAMI AIRPORT                   13054469000    11.27       −− −− −− −− −− −− −−",
        result=result_class(
            layover_city="MIA",
            hotel_name="SONESTA MIAMI AIRPORT",
            hotel_phone="13054469000",
            rest="11.27",
            calendar_entries=["−−", "−−", "−−", "−−", "−−", "−−", "−−"],
        ),
    ),
    ParsingTest[result_class](
        txt="                MIA SONESTA MIAMI AIRPORT                   13054469000    11.27       12 −− −− −− −− −− −−",
        result=result_class(
            layover_city="MIA",
            hotel_name="SONESTA MIAMI AIRPORT",
            hotel_phone="13054469000",
            rest="11.27",
            calendar_entries=["12", "−−", "−−", "−−", "−−", "−−", "−−"],
        ),
    ),
    ParsingTest[result_class](
        txt="                MIA SONESTA MIAMI AIRPORT                                  11.27       −− −− −− −− −− −− −−",
        result=result_class(
            layover_city="MIA",
            hotel_name="SONESTA MIAMI AIRPORT",
            hotel_phone="",
            rest="11.27",
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
