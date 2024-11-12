import logging

import pytest

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.model import IndexedString
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from tests.resources.model import ParserTest

logger = logging.getLogger(__name__)

result_id = "trip_header"
parser = parsers.TripHeader(state=result_id)

items = [
    ParserTest(
        input=IndexedString(
            idx=0,
            txt="SEQ 25064   1 OPS   POSN CA FO                                                         MO TU WE TH FR SA SU",
        ),
        result_id=result_id,
        data={
            "number": "25064",
            "ops_count": "1",
            "positions": ["CA", "FO"],
            "operations": [],
            "qualifications": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=1,
            txt="SEQ 6292    1 OPS   POSN CA FO                SPANISH OPERATION                        MO TU WE TH FR SA SU",
        ),
        result_id=result_id,
        data={
            "number": "6292",
            "ops_count": "1",
            "positions": ["CA", "FO"],
            "operations": ["SPANISH"],
            "qualifications": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=2,
            txt="SEQ 16945   1 OPS   POSN CA FO                SPECIAL QUALIFICATION                    MO TU WE TH FR SA SU",
        ),
        result_id=result_id,
        data={
            "number": "16945",
            "ops_count": "1",
            "positions": ["CA", "FO"],
            "operations": [],
            "qualifications": ["SPECIAL"],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=3,
            txt="SEQ 25018   2 OPS   POSN CA FO                MEXICO QUALIFICATION                     MO TU WE TH FR SA SU",
        ),
        result_id=result_id,
        data={
            "number": "25018",
            "ops_count": "2",
            "positions": ["CA", "FO"],
            "operations": [],
            "qualifications": ["MEXICO"],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=4,
            txt="SEQ 30569   1 OPS   POSN CA FO                                                         New prior month",
        ),
        result_id=result_id,
        data={
            "number": "30569",
            "ops_count": "1",
            "positions": ["CA", "FO"],
            "operations": [],
            "qualifications": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=5,
            txt="SEQ 30890   1 OPS   POSN CA FO                                                         Replaces prior month",
        ),
        result_id=result_id,
        data={
            "number": "30890",
            "ops_count": "1",
            "positions": ["CA", "FO"],
            "operations": [],
            "qualifications": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=6,
            txt="SEQ 19448   1 OPS   POSN CA FO                ST. THOMAS OPERATION                     MO TU WE TH FR SA SU ",
        ),
        result_id=result_id,
        data={
            "number": "19448",
            "ops_count": "1",
            "positions": ["CA", "FO"],
            "operations": ["ST.", "THOMAS"],
            "qualifications": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=7,
            txt="SEQ 265    10 OPS   POSN FB ONLY              GERMAN   OPERATION                       MO TU WE TH FR SA SU ",
        ),
        result_id=result_id,
        data={
            "number": "265",
            "ops_count": "10",
            "positions": ["FB"],
            "operations": ["GERMAN"],
            "qualifications": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=8,
            txt="SEQ 264     4 OPS   POSN FB ONLY                                                       MO TU WE TH FR SA SU ",
        ),
        result_id=result_id,
        data={
            "number": "264",
            "ops_count": "4",
            "positions": ["FB"],
            "operations": [],
            "qualifications": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=9,
            txt="SEQ 657     2 OPS   POSN FO C                                                          MO TU WE TH FR SA SU ",
        ),
        result_id=result_id,
        data={
            "number": "657",
            "ops_count": "2",
            "positions": ["FO", "C"],
            "operations": [],
            "qualifications": [],
        },
    ),
    ParserTest(
        input=IndexedString(
            idx=10,
            txt="SEQ 30097   1 OPS   POSN FB ONLY              JAPANESE OPERATION                       Replaces prior month",
        ),
        result_id=result_id,
        data={
            "number": "30097",
            "ops_count": "1",
            "positions": ["FB"],
            "operations": ["JAPANESE"],
            "qualifications": [],
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
