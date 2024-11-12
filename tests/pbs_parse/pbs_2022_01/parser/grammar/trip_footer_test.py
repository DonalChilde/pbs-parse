from logging import Logger

import pytest

from pbs_parse.pbs_2022_01.parser import grammar
from tests.resources.model import GrammarTest

Items = [
    GrammarTest(
        txt="TTL                                              7.50   0.00   7.50        10.20       −− −− −−",
        result={
            "block": "7.50",
            "synth": "0.00",
            "total_pay": "7.50",
            "tafb": "10.20",
            "calendar_entries": ["−−", "−−", "−−"],
        },
    ),
    # GrammarTest(
    #     txt="",
    #     result={},
    # ),
]
parser = grammar.TripFooter


@pytest.mark.parametrize("test_data", Items)
def test_grammar(logger: Logger, test_data: GrammarTest):
    parse_result = parser.parse_string(test_data.txt)
    result = parse_result.as_dict()  # type: ignore
    print(f"{parse_result}")
    print(f"{result!r}")
    assert result == test_data.result
