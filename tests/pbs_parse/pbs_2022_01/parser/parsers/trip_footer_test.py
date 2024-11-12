import logging

import pytest

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "trip_footer"
parser = parsers.TripFooter(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="TTL                                              7.50   0.00   7.50        10.20       −− −− −−",
        ),
        result_id=result_id,
        data={
            "block": "7.50",
            "synth": "0.00",
            "total_pay": "7.50",
            "tafb": "10.20",
            "calendar_entries": ["−−", "−−", "−−"],
        },
    ),
]


@pytest.mark.parametrize("test_data", items)
def test_parser(logger: logging.Logger, test_data: ParserTest):
    ctx = ParseContext(beginning_state="start")
    parse_result = parser.parse(ctx=ctx, input=test_data.input)
    logger.info(f"{parse_result!r}")
    assert parse_result.current_state == parser.state
    assert parse_result.current_state == result_id
    assert parse_result.result.id == parser.state
    assert parse_result.result.id == result_id
    assert parse_result.result.data == test_data.data
    assert parse_result.result.indexed_string == test_data.input