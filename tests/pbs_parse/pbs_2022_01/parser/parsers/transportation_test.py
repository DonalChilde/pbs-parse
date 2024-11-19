import logging

import pytest
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser import ParseContext

from pbs_parse.pbs_2022_01.parser import parsers
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "transportation"
parser = parsers.Transportation(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="                    SIN FIN DE SERVICIOS                    3331223240",
        ),
        result_id=result_id,
        data={
            "name": "SIN FIN DE SERVICIOS",
            "phone": "3331223240",
            "calendar": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="                    VIP TRANSPORTATION− OGG                 8088712702                 −− −− −−",
        ),
        result_id=result_id,
        data={
            "name": "VIP TRANSPORTATION− OGG",
            "phone": "8088712702",
            "calendar": ["−−", "−−", "−−"],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="                    COMET CAR HIRE (CCH) LTD                442088979984               \u2212\u2212 \u2212\u2212 \u2212\u2212\n",
        ),
        result_id=result_id,
        data={
            "name": "COMET CAR HIRE (CCH) LTD",
            "phone": "442088979984",
            "calendar": ["−−", "−−", "−−"],
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
