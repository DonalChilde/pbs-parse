import pytest

from pbs_parse.pbs_2022_01.parser import grammar
from tests.resources.model import GrammarTest

Items = [
    GrammarTest(
        txt="BOS 737",
        result={"base": "BOS", "equipment": "737"},
    ),
    GrammarTest(
        txt="LAX SAN 737",
        result={"base": "LAX", "satellite_base": "SAN", "equipment": "737"},
    ),
]
parser = grammar.BaseEquipment


@pytest.mark.parametrize("test_data", Items)
def test_grammar(test_data: GrammarTest):
    parse_result = parser.parse_string(test_data.txt)
    result = parse_result.as_dict()  # type: ignore
    print(f"{parse_result}")
    print(f"{result!r}")
    assert result == test_data.result
