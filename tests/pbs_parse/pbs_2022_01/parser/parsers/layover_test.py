import logging

import pytest

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "layover"
parser = parsers.Layover(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="                MIA SONESTA MIAMI AIRPORT                   13054469000    11.27       −− −− −− −− −− −− −−",
        ),
        result_id=result_id,
        data={
            "layover_city": "MIA",
            "hotel": "SONESTA MIAMI AIRPORT",
            "hotel_phone": "13054469000",
            "rest": "11.27",
            "calendar_entries": ["−−", "−−", "−−", "−−", "−−", "−−", "−−"],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="                LHR PARK PLAZA WESTMINSTER BRIDGE LONDON    443334006112   24.00       −− −− −− −− −− −− −−",
        ),
        result_id=result_id,
        data={
            "layover_city": "LHR",
            "hotel": "PARK PLAZA WESTMINSTER BRIDGE LONDON",
            "hotel_phone": "443334006112",
            "rest": "24.00",
            "calendar_entries": ["−−", "−−", "−−", "−−", "−−", "−−", "−−"],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="                JFK HOTEL INFO IN CCI/CREW PORTAL                          19.37\n",
        ),
        result_id=result_id,
        data={
            "layover_city": "JFK",
            "hotel": "HOTEL INFO IN CCI/CREW PORTAL",
            "rest": "19.37",
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
