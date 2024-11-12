import logging

import pytest

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "flight_deadhead"
parser = parsers.FlightDeadhead(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="3  3/3 CE 2308D DFW 1635/1635    AUS 1741/1741    AA    1.06                                                ",
        ),
        result_id=result_id,
        data={
            "dutyperiod": "3",
            "day_of_sequence": "3/3",
            "equipment_code": "CE",
            "flight_number": "2308",
            "deadhead": "D",
            "departure_station": "DFW",
            "departure_time": "1635/1635",
            "crew_meal": "",
            "arrival_station": "AUS",
            "arrival_time": "1741/1741",
            "deadhead_block": "AA",
            "synth": "1.06",
            "ground": "0.00",
            "equipment_change": "",
            "calendar_entries": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=2,
            txt="2  2/2 45 1614D MCI 1607/1407    DFW 1800/1600    AA    1.53   1.27X",
        ),
        result_id=result_id,
        data={
            "dutyperiod": "2",
            "day_of_sequence": "2/2",
            "equipment_code": "45",
            "flight_number": "1614",
            "deadhead": "D",
            "departure_station": "MCI",
            "departure_time": "1607/1407",
            "crew_meal": "",
            "arrival_station": "DFW",
            "arrival_time": "1800/1600",
            "deadhead_block": "AA",
            "synth": "1.53",
            "ground": "1.27",
            "equipment_change": "X",
            "calendar_entries": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=2,
            txt="4  4/4 64 2578D MIA 1949/1649    SAN 2220/2220    AA    5.31",
        ),
        result_id=result_id,
        data={
            "dutyperiod": "4",
            "day_of_sequence": "4/4",
            "equipment_code": "64",
            "flight_number": "2578",
            "deadhead": "D",
            "departure_station": "MIA",
            "departure_time": "1949/1649",
            "crew_meal": "",
            "arrival_station": "SAN",
            "arrival_time": "2220/2220",
            "deadhead_block": "AA",
            "synth": "5.31",
            "ground": "0.00",
            "equipment_change": "",
            "calendar_entries": [],
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
