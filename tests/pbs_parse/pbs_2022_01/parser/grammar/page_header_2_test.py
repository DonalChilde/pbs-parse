import pytest

from pbs_parse.pbs_2022_01.parser import grammar
from tests.resources.model import GrammarTest

Items = [
    GrammarTest(
        txt="DP D/A EQ FLT#  STA DLCL/DHBT ML STA ALCL/AHBT  BLOCK  SYNTH   TPAY   DUTY  TAFB   FDP CALENDAR 05/02−06/01",
        result={"from_date": ["05", "/", "02"], "to_date": ["06", "/", "01"]},
    )
]
parser = grammar.PageHeader2


@pytest.mark.parametrize("test_data", Items)
def test_grammar(test_data: GrammarTest):
    parse_result = parser.parse_string(test_data.txt)
    result = parse_result.as_dict()  # type: ignore
    print(f"{parse_result}")
    print(f"{result!r}")
    assert result == test_data.result
