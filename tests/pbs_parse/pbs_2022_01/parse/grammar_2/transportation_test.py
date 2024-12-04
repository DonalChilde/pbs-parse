"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_TD
from pbs_parse.pbs_2022_01.parse import grammar_2
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar_2.transportation
result_class = grammar_TD.Transportation
test_name = "transportation" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="                    SIN FIN DE SERVICIOS                    3331223240",
        result=result_class(
            name="SIN FIN DE SERVICIOS",
            phone="3331223240",
            calendar_entries=[],
        ),
    ),
    ParsingTest[result_class](
        txt="                    VIP TRANSPORTATION− OGG                 8088712702                 −− −− −−",
        result=result_class(
            name="VIP TRANSPORTATION− OGG",
            phone="8088712702",
            calendar_entries=["−−", "−−", "−−"],
        ),
    ),
    ParsingTest[result_class](
        txt="                    VIP TRANSPORTATION− OGG                                  −− −− −−",
        result=result_class(
            name="VIP TRANSPORTATION− OGG",
            phone="",
            calendar_entries=["−−", "−−", "−−"],
        ),
    ),
    ParsingTest[result_class](
        txt="                    VIP TRANSPORTATION− OGG                                  ",
        result=result_class(
            name="VIP TRANSPORTATION− OGG",
            phone="",
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
