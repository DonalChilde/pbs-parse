"""FILE: is_prior_month.py."""

from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip


def is_prior_month(parsed_trip: ParsedTrip) -> bool:
    """Check to see if the trip is a `prior month` trip."""
    for line in parsed_trip.parsed_lines:
        if "trip_header" == line.id:
            if "prior" not in line.indexed_string.txt:
                return False
    return True
