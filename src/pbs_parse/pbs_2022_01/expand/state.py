"""FILE: state.py."""

from dataclasses import dataclass
from zoneinfo import ZoneInfo

from pbs_parse.pbs_2022_01.models.expanded import AirportCode


@dataclass
class State:
    """State."""

    base: AirportCode
    hbt_tzinfo: ZoneInfo
    dp_idx: int = 0
    flight_idx: int = 0
