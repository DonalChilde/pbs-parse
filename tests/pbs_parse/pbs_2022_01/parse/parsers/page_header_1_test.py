import logging

import pytest
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser import ParseContext

from pbs_parse.pbs_2022_01.parse import parsers
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "page_header_1"
parser = parsers.PageHeader1(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="   DAY          −−DEPARTURE−−    −−−ARRIVAL−−−                GRND/        REST/",
        ),
        result_id=result_id,
        data={},
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
