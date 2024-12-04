"""Tests for state parser.."""

import logging

import pytest
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser import ParseContext
from pfmsoft.state_parser.model import ParsedIndexedString, ParseResult

from pbs_parse.pbs_2022_01.models import grammar_TD
from pbs_parse.pbs_2022_01.parse import parsers_2
from tests.resources.model import ParserTest2

logger = logging.getLogger(__name__)

state = "BaseEquipment"
parser = parsers_2.BaseEquipment(state=state)
result_class = grammar_TD.BaseEquipment
test_name = f"{state} parser "
test_items = [
    ParserTest2[result_class](
        input=IndexedString(
            idx=1,
            txt="BOS 737",
        ),
        result_id=state,
        data=result_class(base="BOS", satellite_base="", equipment="737"),
    ),
    ParserTest2[result_class](
        input=IndexedString(
            idx=2,
            txt="LAX SAN 737",
        ),
        result_id=state,
        data=result_class(base="LAX", satellite_base="SAN", equipment="737"),
    ),
]


def idfn(val: ParserTest2[result_class]) -> str:
    """Return a custom test name for parameterized tests."""
    return test_name


@pytest.mark.parametrize("test_data", test_items, ids=idfn)
def test_grammar(test_data: ParserTest2[result_class]):
    """Parse a string and test against expected result."""
    ctx = ParseContext()
    parse_result = parser.parse(ctx=ctx, input=test_data.input)
    expected = ParseResult(
        current_state=state,
        parsed_indexed_string=ParsedIndexedString(
            id=state,
            indexed_string=test_data.input,
            data=test_data.data,  # type: ignore
        ),
    )
    logger.info(f"Text: {test_data.input!r}")
    logger.info(f"Expected: {expected!r}")
    logger.info(f"Received: {parse_result!r}")
    assert parse_result == expected
