"""FILE: validate_expanded.py."""

from pbs_parse.pbs_2022_01.expand_from_parsed.collate_parsed import collate_parsed
from pbs_parse.pbs_2022_01.expand_from_parsed.validate.check_duty_time import (
    check_duty_time,
)
from pbs_parse.pbs_2022_01.expand_from_parsed.validate.check_localized_times import (
    check_localized_times,
)
from pbs_parse.pbs_2022_01.expand_from_parsed.validate.check_tafb import check_tafb
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip


def validate_expanded_trip(expanded: ExpandedTrip, parsed: ParsedTrip):
    """validate_expanded_trip.

    Args:
        expanded (ExpandedTrip): _description_
        parsed (ParsedTrip): _description_
    """
    collated = collate_parsed(parsed_trip=parsed)

    check_localized_times(expanded=expanded, collated=collated)
    check_tafb(expanded=expanded, collated=collated)
    check_duty_time(expanded=expanded, collated=collated)
