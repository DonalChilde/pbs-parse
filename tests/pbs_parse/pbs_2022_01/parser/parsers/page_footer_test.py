import logging

import pytest
from pfmsoft.snippets.indexed_string.model import IndexedString
from pfmsoft.snippets.state_parser import ParseContext

from pbs_parse.pbs_2022_01.parser import parsers
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "page_footer"
parser = parsers.PageFooter(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="COCKPIT  ISSUED 08APR2022  EFF 02MAY2022               LAX 737  DOM                              PAGE   644",
        ),
        result_id=result_id,
        data={
            "issued": "08APR2022",
            "effective": "02MAY2022",
            "base": "LAX",
            "satelite_base": "",
            "equipment": "737",
            "division": "DOM",
            "internal_page": "644",
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="COCKPIT  ISSUED 08APR2022  EFF 02MAY2022               LAX 320  INTL                             PAGE  1178",
        ),
        result_id=result_id,
        data={
            "issued": "08APR2022",
            "effective": "02MAY2022",
            "base": "LAX",
            "satelite_base": "",
            "equipment": "320",
            "division": "INTL",
            "internal_page": "1178",
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
