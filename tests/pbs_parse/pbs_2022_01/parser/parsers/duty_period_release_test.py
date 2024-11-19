import logging

import pytest
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser import ParseContext

from pbs_parse.pbs_2022_01.parser import parsers
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
            "release": "0739/0439",
            "block": "4.49",
            "synth": "0.00",
            "total_pay": "4.49",
            "duty": "6.19",
            "flight_duty": "5.49",
            "calendar": ["−−", "−−", "−−", "−−", "−−", "−−", "−−"],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=2,
            txt="                                 RLS 2252/2252   0.00   5.46   5.46   6.46        0.00",
        ),
        result_id=result_id,
        data={
            "release": "2252/2252",
            "block": "0.00",
            "synth": "5.46",
            "total_pay": "5.46",
            "duty": "6.46",
            "flight_duty": "0.00",
            "calendar": [],
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
    assert parse_result.parsed_indexed_string.id == parser.state
    assert parse_result.parsed_indexed_string.id == result_id
    assert parse_result.parsed_indexed_string.data == test_data.data
    assert parse_result.parsed_indexed_string.indexed_string == test_data.input
