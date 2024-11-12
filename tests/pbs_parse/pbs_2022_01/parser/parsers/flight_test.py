import logging

import pytest

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "flight"
parser = parsers.Flight(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="1  1/1 65 2131  SAN 1337/1337    ORD 1935/1735   3.58          1.10X                   −− −− −− −− −− −− −−",
        ),
        result_id=result_id,
        data={
            "dutyperiod": "1",
            "day_of_sequence": "1/1",
            "equipment_code": "65",
            "flight_number": "2131",
            "departure_station": "SAN",
            "departure_time": "1337/1337",
            "crew_meal": "",
            "arrival_station": "ORD",
            "arrival_time": "1935/1735",
            "block": "3.58",
            "ground": "1.10",
            "equipment_change": "X",
            "calendar_entries": ["−−", "−−", "−−", "−−", "−−", "−−", "−−"],
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
