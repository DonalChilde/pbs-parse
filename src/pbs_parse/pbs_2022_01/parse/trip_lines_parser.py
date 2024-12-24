"""Parser for TripLines."""

from pathlib import Path

from pfmsoft.state_parser import ParseContext, ParseScheme, StateParser
from pfmsoft.state_parser.parse_exception import ParseException
from pfmsoft.state_parser.result_handler import CollectResults

from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TRIP_LINES_SERIALIZER, TripLines
from pbs_parse.pbs_2022_01.parse.parse_table import parse_table


class TripLinesParser:
    """Parser for TripLines."""

    def __init__(self, scheme: ParseScheme | None = None) -> None:
        """Parser for TripLines."""
        if scheme is None:
            scheme = ParseScheme(beginning_state="start", parser_lookup=parse_table())
        self.scheme = scheme

    def parse_file(self, ctx: ParseContext, path_in: Path) -> ParsedTrip:
        """Parse TripLines from file."""
        trip_lines = TRIP_LINES_SERIALIZER.load_from_json(path_in=path_in)
        return self.parse(ctx=ctx, trip_lines=trip_lines)

    def parse(self, ctx: ParseContext, trip_lines: TripLines) -> ParsedTrip:
        """Parse TripLines."""
        handler = CollectResults()
        parser = StateParser(parse_scheme=self.scheme, result_handler=handler)
        try:
            parser.parse(ctx=ctx, data=trip_lines.lines)
        except ParseException as e:
            print(e)

        trip = ParsedTrip(
            source=trip_lines.uuid,
            page_idx=trip_lines.page_idx,
            trip_idx=trip_lines.idx,
            parsed_lines=[x.parsed_indexed_string for x in handler.results],
        )
        return trip
