"""FILE: bid_data.py."""

from dataclasses import dataclass
from typing import TypedDict

from whenever import Date


class EffectiveTD(TypedDict):
    """EffectiveTD."""

    start: str
    end: str


@dataclass(slots=True)
class Effective:
    """Effective."""

    start: Date
    end: Date

    @staticmethod
    def from_simple(value: EffectiveTD) -> "Effective":
        """from_simple."""
        return Effective(
            start=Date.parse_common_iso(value["start"]),
            end=Date.parse_common_iso(value["end"]),
        )

    def to_simple(self) -> EffectiveTD:
        """to_simple."""
        return EffectiveTD(start=str(self.start), end=str(self.end))


class BidDataTD(TypedDict):
    """BidDataTD."""

    name: str
    base: str
    effective: EffectiveTD


@dataclass(slots=True, kw_only=True)
class BidData:
    """BidData."""

    name: str
    base: str
    effective: Effective

    def to_simple(self) -> BidDataTD:
        """To simple."""
        return BidDataTD(
            name=self.name, base=self.base, effective=self.effective.to_simple()
        )

    @staticmethod
    def from_simple(value: BidDataTD) -> "BidData":
        """From simple."""
        return BidData(
            name=value["name"],
            base=value["base"],
            effective=Effective.from_simple(value["effective"]),
        )
