import logging

import pytest

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
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
