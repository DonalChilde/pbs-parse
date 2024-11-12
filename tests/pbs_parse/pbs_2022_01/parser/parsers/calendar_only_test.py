import logging

import pytest

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
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
        data={"calendar_entries": ["−−", "17", "18", "19", "20", "21", "22"]},
    ),
    ParserTest(
        input=IndexedString(
            idx=2,
            txt="                                                                                       23 24 25 26 27 28 29",
        ),
        result_id=result_id,
        data={"calendar_entries": ["23", "24", "25", "26", "27", "28", "29"]},
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
