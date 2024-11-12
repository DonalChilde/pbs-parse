from importlib import resources
from logging import Logger
from pathlib import Path

import pytest

from pbs_parse.pbs_2022_01.parser.parse_table import parse_table
from pbs_parse.snippets.indexed_string.model import IndexedStrings
from pbs_parse.snippets.indexed_string.state_parser.model import ParseResults
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from pbs_parse.snippets.indexed_string.state_parser.parse_scheme import ParseScheme
from pbs_parse.snippets.indexed_string.state_parser.result_handler import (
    SaveResultsToFile,
)
from pbs_parse.snippets.indexed_string.state_parser.state_parser import StateParser
from tests.resources.model import ParseTripTest
from tests.resources.trips import TRIPS_INDEXED_ANCHOR, TRIPS_PARSED_ANCHOR

OUTPUT_PATH = f"trips/parsed/{Path(__file__).stem}"

items = [
    ParseTripTest(
        indexed_anchor=TRIPS_INDEXED_ANCHOR,
        indexed_filename="PBS_DFW_November_2024_20241010125734.page_8_of_1096.trip_3_of_5.json",
        parsed_anchor=TRIPS_PARSED_ANCHOR,
        parsed_filename="PBS_DFW_November_2024_20241010125734.page_8_of_1096.trip_3_of_5.parsed.json",
    )
]

PARSE_ONLY = False


@pytest.mark.parametrize("parse_trips_one", items)
def test_parse_trips(
    logger: Logger, test_output_dir: Path, parse_trips_one: ParseTripTest
):
    indexed_file = resources.files(parse_trips_one.indexed_anchor).joinpath(
        parse_trips_one.indexed_filename
    )
    with resources.as_file(indexed_file) as input_path:
        data = IndexedStrings.from_file(file_path=input_path)
        path_out = test_output_dir / OUTPUT_PATH / f"{input_path.stem}.parsed.json"
    scheme = ParseScheme(beginning_state="start", parser_lookup=parse_table())
    ctx = ParseContext()
    handler = SaveResultsToFile(path_out=path_out)
    parser = StateParser(parse_scheme=scheme, result_handler=handler)
    parser.parse(ctx=ctx, data=data.strings)
    results = handler.results
    assert results.results
    if not PARSE_ONLY:
        parsed_file = resources.files(parse_trips_one.parsed_anchor).joinpath(
            parse_trips_one.parsed_filename
        )
        with resources.as_file(parsed_file) as input_path:
            parsed = ParseResults.from_file(file_path=input_path)
            assert results == parsed
