import pytest

from pbs_parse.pbs_2022_01.parser import grammar
from tests.resources.model import GrammarTest

Items = [
    GrammarTest(
        txt="COCKPIT  ISSUED 08APR2022  EFF 02MAY2022               LAX 737  DOM                              PAGE   644",
        result={
            "issued": "08APR2022",
            "effective": "02MAY2022",
            "base": "LAX",
            "satelite_base": "",
            "equipment": "737",
            "division": "DOM",
            "internal_page": "644",
        },
    ),
    GrammarTest(
        txt="COCKPIT  ISSUED 08APR2022  EFF 02MAY2022               LAX 320  INTL                             PAGE  1178",
        result={
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
parser = grammar.PageFooter


@pytest.mark.parametrize("test_data", Items)
def test_grammar(test_data: GrammarTest):
    parse_result = parser.parse_string(test_data.txt)
    result = parse_result.as_dict()  # type: ignore
    print(f"{parse_result}")
    print(f"{result!r}")
    assert result == test_data.result
