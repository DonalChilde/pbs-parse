import logging

import pytest

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "base_equipment"
parser = parsers.BaseEquipment(state=result_id)

items = [
    ParserTest(
        input=IndexedString(idx=1, txt="BOS 737"),
        result_id=result_id,
        data={"base": "BOS", "equipment": "737"},
    ),
    ParserTest(
        input=IndexedString(idx=2, txt="LAX SAN 737"),
        result_id=result_id,
        data={"base": "LAX", "satellite_base": "SAN", "equipment": "737"},
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
