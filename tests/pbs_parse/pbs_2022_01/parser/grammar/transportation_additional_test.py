import pytest

from pbs_parse.pbs_2022_01.parser import grammar
from tests.resources.model import GrammarTest

Items = [
    GrammarTest(
        txt="                    SKY TRANSPORTATION SERVICE, LLC         8566169633",
        result={
            "transportation": "SKY TRANSPORTATION SERVICE, LLC",
            "phone": "8566169633",
            "calendar_entries": [],
        },
    ),
    GrammarTest(
        txt="                    DESERT COACH                            6022866161                    ",
        result={
            "transportation": "DESERT COACH",
            "phone": "6022866161",
            "calendar_entries": [],
        },
    ),
]
parser = grammar.TransportationAdditional


@pytest.mark.parametrize("test_data", Items)
def test_grammar(test_data: GrammarTest):
    parse_result = parser.parse_string(test_data.txt)
    result = parse_result.as_dict()  # type: ignore
    print(f"{parse_result}")
    print(f"{result!r}")
    assert result == test_data.result
