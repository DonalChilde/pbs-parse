from pathlib import Path
from typing import Optional

from pbs_split.models import TripLines, trip_lines_serializer
from pfmsoft.state_parser import ParseContext, ParseScheme, StateParser
from pfmsoft.state_parser.parse_exception import ParseException
from pfmsoft.state_parser.result_handler import CollectResults

from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.parser.parse_table import parse_table


class TripLinesParser:
    def __init__(self, scheme: Optional[ParseScheme] = None) -> None:
        if scheme is None:
            scheme = ParseScheme(parser_lookup=parse_table())
        self.scheme = scheme

    def parse_file(self, ctx: ParseContext, path_in: Path) -> ParsedTrip:
        serializer = trip_lines_serializer()
        trip_lines = serializer.load_from_json(path_in=path_in)
        return self.parse(ctx=ctx, trip_lines=trip_lines)

    def parse(self, ctx: ParseContext, trip_lines: TripLines) -> ParsedTrip:
        handler = CollectResults()
        parser = StateParser(parse_scheme=self.scheme, result_handler=handler)
        try:
            parser.parse(ctx=ctx, data=trip_lines.lines)
        except ParseException as e:
            print(e)

        trip = ParsedTrip(
            source=trip_lines.uuid,
            parsed_lines=[x.parsed_indexed_string for x in handler.results],
        )
        return trip
