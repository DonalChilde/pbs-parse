import logging

import pytest

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "transportation_additional"
parser = parsers.TransportationAdditional(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="                    SKY TRANSPORTATION SERVICE, LLC         8566169633",
        ),
        result_id=result_id,
        data={
            "transportation": "SKY TRANSPORTATION SERVICE, LLC",
            "phone": "8566169633",
            "calendar_entries": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="                    DESERT COACH                            6022866161                    ",
        ),
        result_id=result_id,
        data={
            "transportation": "DESERT COACH",
            "phone": "6022866161",
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
