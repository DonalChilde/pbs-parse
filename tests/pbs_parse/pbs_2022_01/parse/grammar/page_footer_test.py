"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_td
from pbs_parse.pbs_2022_01.parse import grammar
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar.page_footer
result_class = grammar_td.PageFooter
test_name = "page_footer" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="COCKPIT  ISSUED 08APR2022  EFF 02MAY2022               LAX 737  DOM                              PAGE   644",
        result=result_class(
            issued="08APR2022",
            effective="02MAY2022",
            base="LAX",
            satellite_base="",
            equipment="737",
            division="DOM",
            page="644",
        ),
    ),
    ParsingTest[result_class](
        txt="COCKPIT  ISSUED 08APR2022  EFF 02MAY2022               LAX 320  INTL                             PAGE  1178",
        result=result_class(
            issued="08APR2022",
            effective="02MAY2022",
            base="LAX",
            satellite_base="",
            equipment="320",
            division="INTL",
            page="1178",
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
