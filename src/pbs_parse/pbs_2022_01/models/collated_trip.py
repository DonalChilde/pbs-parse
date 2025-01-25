"""FILE: collated_trip.py."""

from dataclasses import dataclass, field

from pfmsoft.state_parser.model import ParsedIndexedString


@dataclass(slots=True, kw_only=True)
class CollatedDutyPeriod:
    """CollatedDutyPeriod."""

    report: ParsedIndexedString
    flights: list[ParsedIndexedString] = field(default_factory=list)
    release: ParsedIndexedString
    layover: ParsedIndexedString | None
    hotel: list[ParsedIndexedString] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class CollatedTrip:
    """CollatedTrip."""

    page_header_1: ParsedIndexedString
    page_header_2: ParsedIndexedString
    trip_header: ParsedIndexedString
    dutyperiods: list[CollatedDutyPeriod] = field(default_factory=list)
    trip_footer: ParsedIndexedString
    page_footer: ParsedIndexedString
