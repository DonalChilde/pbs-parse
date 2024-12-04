"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_TD
from pbs_parse.pbs_2022_01.parse import grammar_2
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar_2.base_equipment
result_class = grammar_TD.BaseEquipment
test_name = "base_equipment" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="BOS 737",
        result=result_class(base="BOS", satellite_base="", equipment="737"),
    ),
    ParsingTest[result_class](
        txt="LAX SAN 737",
        result=result_class(base="LAX", satellite_base="SAN", equipment="737"),
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
