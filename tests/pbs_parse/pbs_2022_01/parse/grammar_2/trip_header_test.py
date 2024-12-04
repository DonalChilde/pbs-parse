"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_TD
from pbs_parse.pbs_2022_01.parse import grammar_2
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar_2.trip_header
result_class = grammar_TD.TripHeader
test_name = "trip_header" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="SEQ 25064   1 OPS   POSN CA FO                                                         MO TU WE TH FR SA SU",
        result=result_class(
            trip_number="25064",
            ops_count="1",
            positions=["CA", "FO"],
            operations=[],
            special_qual=False,
            prior_month_trip=False,
        ),
    ),
    ParsingTest[result_class](
        txt="SEQ 16945   1 OPS   POSN CA FO                SPECIAL QUALIFICATION                    MO TU WE TH FR SA SU",
        result=result_class(
            trip_number="16945",
            ops_count="1",
            positions=["CA", "FO"],
            operations=[],
            special_qual=True,
            prior_month_trip=False,
        ),
    ),
    ParsingTest[result_class](
        txt="SEQ 6292    1 OPS   POSN CA FO                SPANISH OPERATION                        MO TU WE TH FR SA SU",
        result=result_class(
            trip_number="6292",
            ops_count="1",
            positions=["CA", "FO"],
            operations=["SPANISH"],
            special_qual=False,
            prior_month_trip=False,
        ),
    ),
    ParsingTest[result_class](
        txt="SEQ 30097   1 OPS   POSN FB ONLY              JAPANESE OPERATION                       Replaces prior month",
        result=result_class(
            trip_number="30097",
            ops_count="1",
            positions=["FB"],
            operations=["JAPANESE"],
            special_qual=False,
            prior_month_trip=True,
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
