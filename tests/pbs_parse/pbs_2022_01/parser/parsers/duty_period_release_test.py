import logging

import pytest

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "dutyperiod_release"
parser = parsers.DutyPeriodRelease(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="                                 RLS 0739/0439   4.49   0.00   4.49   6.19        5.49 −− −− −− −− −− −− −−",
        ),
        result_id=result_id,
        data={
            "release_time": "0739/0439",
            "block": "4.49",
            "synth": "0.00",
            "total_pay": "4.49",
            "duty": "6.19",
            "flight_duty": "5.49",
            "calendar_entries": ["−−", "−−", "−−", "−−", "−−", "−−", "−−"],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=2,
            txt="                                 RLS 2252/2252   0.00   5.46   5.46   6.46        0.00",
        ),
        result_id=result_id,
        data={
            "release_time": "2252/2252",
            "block": "0.00",
            "synth": "5.46",
            "total_pay": "5.46",
            "duty": "6.46",
            "flight_duty": "0.00",
            "calendar_entries": [],
        },
    ),
]


@pytest.mark.parametrize("test_data", items)
def test_parser(test_data: ParserTest):
    ctx = ParseContext()
    parse_result = parser.parse(ctx=ctx, input=test_data.input)
    logger.info(f"{parse_result!r}")
    assert parse_result.current_state == parser.state
    assert parse_result.current_state == result_id
    assert parse_result.result.id == parser.state
    assert parse_result.result.id == result_id
    assert parse_result.result.data == test_data.data
    assert parse_result.result.indexed_string == test_data.input
