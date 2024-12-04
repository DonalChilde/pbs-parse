"""Tests for pyparsing grammar."""

import logging

import pytest

from pbs_parse.pbs_2022_01.models import grammar_TD
from pbs_parse.pbs_2022_01.parse import grammar_2
from tests.resources.model import ParsingTest

logger = logging.getLogger(__name__)

parser = grammar_2.flight_deadhead
result_class = grammar_TD.Flight
test_name = "flight_deadhead" + " grammar "
test_items = [
    ParsingTest[result_class](
        txt="3  3/3 CE 2308D DFW 1635/1635    AUS 1741/1741    AA    1.06",
        result=result_class(
            dutyperiod_idx="3",
            depart_day="3",
            arrive_day="3",
            equipment_code="CE",
            flight_number="2308",
            deadhead=True,
            deadhead_code="AA",
            departure_station="DFW",
            departure_time=grammar_TD.DualTime(lcl="1635", hbt="1635"),
            crew_meal="",
            arrival_station="AUS",
            arrival_time=grammar_TD.DualTime(lcl="1741", hbt="1741"),
            block="0.00",
            synth="1.06",
            ground="0.00",
            equipment_change=False,
            calendar_entries=[],
        ),
    ),
    ParsingTest[result_class](
        txt="2  2/2 45 1614D MCI 1607/1407    DFW 1800/1600    AA    1.53   1.27X",
        result=result_class(
            dutyperiod_idx="2",
            depart_day="2",
            arrive_day="2",
            equipment_code="45",
            flight_number="1614",
            deadhead=True,
            deadhead_code="AA",
            departure_station="MCI",
            departure_time=grammar_TD.DualTime(lcl="1607", hbt="1407"),
            crew_meal="",
            arrival_station="DFW",
            arrival_time=grammar_TD.DualTime(lcl="1800", hbt="1600"),
            block="0.00",
            synth="1.53",
            ground="1.27",
            equipment_change=True,
            calendar_entries=[],
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
