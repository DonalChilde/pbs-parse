import logging

import pytest
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser import ParseContext

from pbs_parse.pbs_2022_01.parse import parsers
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "page_header_2"
parser = parsers.PageHeader2(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="DP D/A EQ FLT#  STA DLCL/DHBT ML STA ALCL/AHBT  BLOCK  SYNTH   TPAY   DUTY  TAFB   FDP CALENDAR 05/02−06/01",
        ),
        result_id=result_id,
        data={"from_date": "05/02", "to_date": "06/01"},
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
