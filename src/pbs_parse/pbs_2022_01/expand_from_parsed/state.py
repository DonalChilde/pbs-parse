"""FILE: state.py."""

from dataclasses import dataclass, field
from zoneinfo import ZoneInfo

from whenever import Date

from pbs_parse.pbs_2022_01.models.bid_data import BidData
from pbs_parse.pbs_2022_01.models.expanded import AirportInfo
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTripSource


@dataclass(slots=True, kw_only=True)
class State:
    """State."""

    base: AirportInfo
    hbt_tzinfo: ZoneInfo
    dp_idx: int = 0
    flight_idx: int = 0
    source_file: str = ""
    start_dates: list[Date] = field(default_factory=list)
    parsed_source: ParsedTripSource
    bid: BidData

    def reset(self):
        """Reset the dp and flight counters before each trip expansion."""
        self.dp_idx = 0
        self.flight_idx = 0
