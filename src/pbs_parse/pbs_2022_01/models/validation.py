from dataclasses import dataclass, field
from datetime import date

from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.structured import StructuredTrip


@dataclass(slots=True)
class Context:
    parsed_trip: ParsedTrip
    structured_trip: StructuredTrip
    external_start_dates: list[date] = field(default_factory=list)
    parsed_path: str = ""
    structured_path: str = ""
    errors: list[str] = field(default_factory=list)
