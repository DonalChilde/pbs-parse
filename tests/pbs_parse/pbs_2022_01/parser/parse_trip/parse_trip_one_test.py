from importlib import resources
from pathlib import Path

import pytest
from pbs_split.models import trip_lines_serializer
from pfmsoft.snippets.state_parser import ParseContext, ParseScheme

from pbs_parse.pbs_2022_01.models.parsed_trip import parsed_trip_serializer
from pbs_parse.pbs_2022_01.parser.parse_table import parse_table
from pbs_parse.pbs_2022_01.parser.trip_lines_parser import TripLinesParser
from tests.resources.model import FileBasedTest
from tests.resources.trips import TRIPS_INDEXED_ANCHOR, TRIPS_PARSED_ANCHOR

OUTPUT_PATH = f"trips/parsed/{Path(__file__).stem}"

items = [
    FileBasedTest(
        input_anchor=TRIPS_INDEXED_ANCHOR,
        input_filename="PBS_DFW_November_2024_20241010125734.page_8_of_1096.trip_3_of_5.json",
        comparison_anchor=TRIPS_PARSED_ANCHOR,
        comparison_filename="PBS_DFW_November_2024_20241010125734.page_8_of_1096.trip_3_of_5.parsed.json",
    )
]

PARSE_ONLY = False


@pytest.mark.parametrize("parse_trips_one", items)
def test_parse_trips(test_output_dir: Path, parse_trips_one: FileBasedTest):
    indexed_file = resources.files(parse_trips_one.input_anchor).joinpath(
        parse_trips_one.input_filename
    )
    raw_trip_serializer = trip_lines_serializer()
    with resources.as_file(indexed_file) as input_path:
        raw_trip = raw_trip_serializer.load_from_json(path_in=input_path)
        path_out = test_output_dir / OUTPUT_PATH / f"{input_path.stem}.parsed.json"
    scheme = ParseScheme(beginning_state="start", parser_lookup=parse_table())
    ctx = ParseContext()
    parser = TripLinesParser(scheme=scheme)
    parsed_trip = parser.parse(ctx=ctx, trip_lines=raw_trip)
    parsed_serializer = parsed_trip_serializer()
    parsed_serializer.save_as_json(path_out=path_out, complex_obj=parsed_trip)
    if not PARSE_ONLY:
        parsed_file = resources.files(parse_trips_one.comparison_anchor).joinpath(
            parse_trips_one.comparison_filename
        )
        with resources.as_file(parsed_file) as input_path:
            loaded_parsed_trip = parsed_serializer.load_from_json(path_in=input_path)
            assert parsed_trip.parsed_lines[4] == loaded_parsed_trip.parsed_lines[4]
