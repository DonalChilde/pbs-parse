"""FILE: page_lines_td.py."""

from typing import TypedDict

from pbs_parse.pbs_2022_01.models.bid_data_td import BidDataTD
from pbs_parse.snippets.indexed_string.model import IndexedStringTD


class PageLinesSourceTD(TypedDict):
    """PageLinesSourceTD."""

    txt_file: str


class PageLinesTD(TypedDict):
    """PageLinesTD."""

    source: PageLinesSourceTD
    bid: BidDataTD
    idx: str
    lines: list[IndexedStringTD]
