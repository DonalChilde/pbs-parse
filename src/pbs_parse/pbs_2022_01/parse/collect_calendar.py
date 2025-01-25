"""FILE: collect_calendar.py."""

from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip


def collect_calendar(parsed_trip: ParsedTrip) -> list[str]:
    """collect_calendar.

    Args:
        parsed_trip (ParsedTrip): _description_

    Returns:
        list[str]: _description_
    """
    calendar: list[str] = []
    for parsed_line in parsed_trip.parsed_lines:
        maybe = parsed_line.data.get("calendar_entries", [])
        if maybe:
            calendar.extend(maybe)
    return calendar
