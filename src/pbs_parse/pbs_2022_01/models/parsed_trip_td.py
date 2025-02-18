"""FILE: parsed_trip_td.py."""

from typing import TypedDict

from pbs_parse.pbs_2022_01.models.bid_data_td import BidDataTD
from pbs_parse.snippets.indexed_string_state_parser.model import ParsedIndexedStringTD


class ParsedTripSourceTD(TypedDict):
    """ParsedTripSourceTD."""

    txt_file: str
    page_lines: str
    trip_lines: str


class ParsedTripTD(TypedDict):
    """A simple object version of ParsedTrip."""

    source: ParsedTripSourceTD
    bid: BidDataTD
    idx: str
    parsed_lines: list[ParsedIndexedStringTD]
    calendar_entries: list[str]
    start_dates: list[str]
    errors: list[str]
