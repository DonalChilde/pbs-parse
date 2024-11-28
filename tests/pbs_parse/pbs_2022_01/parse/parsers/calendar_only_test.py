import logging

import pytest
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser import ParseContext

from pbs_parse.pbs_2022_01.parse import parsers
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "calendar_only"
parser = parsers.CalendarOnly(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="                                                                                       −− 17 18 19 20 21 22",
        ),
        result_id=result_id,
        data={"calendar": ["−−", "17", "18", "19", "20", "21", "22"]},
    ),
    ParserTest(
        input=IndexedString(
            idx=2,
            txt="                                                                                       23 24 25 26 27 28 29",
        ),
        result_id=result_id,
        data={"calendar": ["23", "24", "25", "26", "27", "28", "29"]},
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
