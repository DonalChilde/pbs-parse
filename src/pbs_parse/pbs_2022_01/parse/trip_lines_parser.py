"""Parser for TripLines."""

from copy import deepcopy

from pbs_parse.common.is_prior_month import is_prior_month
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip, ParsedTripSource
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines
from pbs_parse.pbs_2022_01.parse.build_start_dates import build_start_dates
from pbs_parse.pbs_2022_01.parse.collect_calendar import collect_calendar
from pbs_parse.pbs_2022_01.parse.parse_table import parse_table
from pbs_parse.snippets.indexed_string_state_parser import (
    ParseContext,
    ParseScheme,
    parse,
)
from pbs_parse.snippets.indexed_string_state_parser.exceptions import ParseException
from pbs_parse.snippets.indexed_string_state_parser.result_handlers import (
    CollectResults,
)

# class TripLinesParser:
#     """Parser for TripLines."""

#     def __init__(self, scheme: ParseScheme | None = None) -> None:
#         """Parser for TripLines."""
#         if scheme is None:
#             scheme = ParseScheme(parser_lookup=parse_table())
#         self.scheme = scheme

#     def parse_file(self, ctx: ParseContext, path_in: Path) -> ParsedTrip:
#         """Parse TripLines from file."""
#         trip_lines = TRIP_LINES_SERIALIZER.load_from_json(path_in=path_in)
#         return self.parse(ctx=ctx, trip_lines=trip_lines)

#     def parse(self, ctx: ParseContext, trip_lines: TripLines) -> ParsedTrip:
#         """Parse TripLines."""
#         handler = CollectResults()
#         parser = StateParser(parse_scheme=self.scheme, result_handler=handler)
#         try:
#             parser.parse(ctx=ctx, data=trip_lines.lines)
#         except ParseException as e:
#             print(f"Error parsing {trip_lines.default_file_name()}, error={e}")
#             raise e
#         _source = ParsedTripSource(
#             txt_file=trip_lines.source.txt_file,
#             page_lines=trip_lines.source.page_lines,
#             trip_lines=trip_lines.default_file_name(),
#         )
#         trip = ParsedTrip(
#             source=_source,
#             bid=deepcopy(trip_lines.bid),
#             idx=trip_lines.idx,
#             parsed_lines=[x.parsed_indexed_string for x in handler.results],
#         )
#         if not is_prior_month(parsed_trip=trip):
#             trip.calendar_entries = collect_calendar(parsed_trip=trip)
#             trip.start_dates = build_start_dates(
#                 effective_from=trip.bid.effective.start,
#                 effective_to=trip.bid.effective.end,
#                 calendar=trip.calendar_entries,
#             )
#         return trip


SCHEME = ParseScheme(parser_lookup=parse_table())


def parse_trip(ctx: ParseContext, trip: TripLines) -> ParsedTrip:
    """Parse TripLines."""
    handler = CollectResults()
    try:
        parse(ctx=ctx, data=trip.lines, parse_scheme=SCHEME, result_handler=handler)
    except ParseException as e:
        print(f"Error parsing {trip.default_file_name()}, error={e}")
        raise e
    _source = ParsedTripSource(
        txt_file=trip.source.txt_file,
        page_lines=trip.source.page_lines,
        trip_lines=trip.default_file_name(),
    )
    parsed = ParsedTrip(
        source=_source,
        bid=deepcopy(trip.bid),
        idx=trip.idx,
        parsed_lines=[x.parsed_indexed_string for x in handler.results],
    )
    if not is_prior_month(parsed_trip=parsed):
        parsed.calendar_entries = collect_calendar(parsed_trip=parsed)
        parsed.start_dates = build_start_dates(
            effective_from=trip.bid.effective.start,
            effective_to=trip.bid.effective.end,
            calendar=parsed.calendar_entries,
        )
    return parsed
