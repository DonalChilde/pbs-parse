import logging

import pytest
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser import ParseContext

from pbs_parse.pbs_2022_01.parser import parsers
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
            "dutyperiod_idx": "1",
            "dep_arr_day": "1/1",
            "eq_code": "65",
            "flight_number": "2131",
            "deadhead": "",
            "deadhead_code": "",
            "departure_station": "SAN",
            "departure_time": "1337/1337",
            "crew_meal": "",
            "arrival_station": "ORD",
            "arrival_time": "1935/1735",
            "block": "3.58",
            "synth": "",
            "ground": "1.10",
            "equipment_change": "X",
            "calendar": ["−−", "−−", "−−", "−−", "−−", "−−", "−−"],
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
