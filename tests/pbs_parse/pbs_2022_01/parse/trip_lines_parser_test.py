"""Test the TripLinesParser."""

from importlib import resources
from pathlib import Path

import pytest
from pfmsoft.state_parser import ParseContext, ParseScheme

from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER
from pbs_parse.pbs_2022_01.models.split import TRIP_LINES_SERIALIZER
from pbs_parse.pbs_2022_01.parse.parse_table import parse_table
from pbs_parse.pbs_2022_01.parse.trip_lines_parser import TripLinesParser
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
def test_parse_trip(test_output_dir: Path, parse_trips_one: FileBasedTest):
    trip_lines_resource_file = resources.files(parse_trips_one.input_anchor).joinpath(
        parse_trips_one.input_filename
    )
    with resources.as_file(trip_lines_resource_file) as input_path:
        trip_lines = TRIP_LINES_SERIALIZER.load_from_json(path_in=input_path)
        path_out = test_output_dir / OUTPUT_PATH / f"{input_path.stem}.parsed.json"
    # setup parser
    scheme = ParseScheme(beginning_state="start", parser_lookup=parse_table())
    ctx = ParseContext()
    parser = TripLinesParser(scheme=scheme)

    # parse and save trip
    parsed_trip = parser.parse(ctx=ctx, trip_lines=trip_lines)
    PARSED_TRIP_SERIALIZER.save_as_json(path_out=path_out, complex_obj=parsed_trip)

    # save the string version of parsed trip for debug
    path_out.with_suffix(".txt").write_text(str(parsed_trip))
    if not PARSE_ONLY:
        # load and compare a previous parse.
        parsed_trip_resource_file = resources.files(
            parse_trips_one.comparison_anchor
        ).joinpath(parse_trips_one.comparison_filename)
        with resources.as_file(parsed_trip_resource_file) as input_path:
            loaded_parsed_trip = PARSED_TRIP_SERIALIZER.load_from_json(
                path_in=input_path
            )
            assert parsed_trip.parsed_lines[4] == loaded_parsed_trip.parsed_lines[4]
