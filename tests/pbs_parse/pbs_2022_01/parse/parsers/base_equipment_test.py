import logging

import pytest
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser import ParseContext

from pbs_parse.pbs_2022_01.parse import parsers
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "base_equipment"
parser = parsers.BaseEquipment(state=result_id)

items = [
    ParserTest(
        input=IndexedString(idx=1, txt="BOS 737"),
        result_id=result_id,
        data={"base": "BOS", "satellite_base": "", "equipment": "737"},
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
    assert parse_result.parsed_indexed_string.id == parser.state
    assert parse_result.parsed_indexed_string.id == result_id
    assert parse_result.parsed_indexed_string.data == test_data.data
    assert parse_result.parsed_indexed_string.indexed_string == test_data.input
