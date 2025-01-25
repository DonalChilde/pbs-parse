"""FILE: parsed_to_expanded.py."""

from pathlib import Path
from typing import Self
from zoneinfo import ZoneInfo

from pbs_parse.common.get_airport_info import get_airport_info_from_iata
from pbs_parse.pbs_2022_01.expand_from_parsed.collate_parsed import collate_parsed
from pbs_parse.pbs_2022_01.expand_from_parsed.state import State
from pbs_parse.pbs_2022_01.expand_from_parsed.translate_trips import translate_trips
from pbs_parse.pbs_2022_01.expand_from_parsed.validate.validate_expanded import (
    validate_expanded_trip,
)
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER, ParsedTrip


class ParsedToExpanded:
    """ParsedToExpanded."""

    def __init__(self, parsed_trip: ParsedTrip, source_file: str) -> None:
        """__init__.

        Args:
            parsed_trip (ParsedTrip): _description_
            source_file (str): _description_
        """
        self.parsed = parsed_trip
        self.collated = collate_parsed(parsed_trip=self.parsed)
        self.source_file = source_file
        base = get_airport_info_from_iata(self.collated.page_footer.data["base"])
        self.state = State(
            base=base,
            hbt_tzinfo=ZoneInfo(base.tz_name),
            source_file=source_file,
            start_dates=self.parsed.start_dates,
            parsed_source=self.parsed.source,
        )

    @classmethod
    def from_file(cls, path_in: Path) -> Self:
        """from_file.

        Args:
            path_in (Path): _description_

        Returns:
            StructuredToExpanded: _description_
        """
        return cls(
            parsed_trip=PARSED_TRIP_SERIALIZER.load_from_json(path_in=path_in),
            source_file=path_in.name,
        )

    def translate(self) -> list[ExpandedTrip]:
        """Translate a pbs_2022_01 structured trip to Trip."""
        expanded_trips = translate_trips(collated_trip=self.collated, state=self.state)
        for trip in expanded_trips:
            validate_expanded_trip(expanded=trip, parsed=self.parsed)
        return expanded_trips
