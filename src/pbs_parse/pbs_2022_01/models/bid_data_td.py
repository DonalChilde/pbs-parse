"""FILE: bid_data_td.py."""

from typing import TypedDict


class EffectiveTD(TypedDict):
    """EffectiveTD."""

    start: str
    end: str


class BidDataTD(TypedDict):
    """BidDataTD."""

    name: str
    base: str
    effective: EffectiveTD
