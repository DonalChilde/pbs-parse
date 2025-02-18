"""FILE: trip_lines_td.py."""

from typing import TypedDict

from pbs_parse.pbs_2022_01.models.bid_data_td import BidDataTD
from pbs_parse.snippets.indexed_string import IndexedStringTD


class TripLinesSourceTD(TypedDict):
    """TripLinesSourceTD."""

    txt_file: str
    page_lines: str


class TripLinesTD(TypedDict):
    """TripLinesTD."""

    source: TripLinesSourceTD
    bid: BidDataTD
    idx: str
    lines: list[IndexedStringTD]
