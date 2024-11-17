import logging

import pytest
from pfmsoft.snippets.indexed_string.model import IndexedString
from pfmsoft.snippets.state_parser import ParseContext

from pbs_parse.pbs_2022_01.parser import parsers
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "hotel_additional"
parser = parsers.HotelAdditional(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="               +PHL MARRIOTT OLD CITY                       12152386000",
        ),
        result_id=result_id,
        data={
            "layover_city": "PHL",
            "name": "MARRIOTT OLD CITY",
            "phone": "12152386000",
            "calendar": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="               +PHL CAMBRIA HOTEL AND SUITES                12157325500",
        ),
        result_id=result_id,
        data={
            "layover_city": "PHL",
            "name": "CAMBRIA HOTEL AND SUITES",
            "phone": "12157325500",
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
