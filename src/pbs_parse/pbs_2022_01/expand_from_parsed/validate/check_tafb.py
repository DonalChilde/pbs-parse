"""FILE: check_tafb.py."""

from pbs_parse.common.parse_duration_whenever import parse_duration
from pbs_parse.pbs_2022_01.models.collated_trip import CollatedTrip
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip


def check_tafb(expanded: ExpandedTrip, collated: CollatedTrip) -> None:
    """check_tafb.

    Args:
        expanded (ExpandedTrip): _description_
        collated (CollatedTrip): _description_
    """
    expanded_tafb = expanded.tafb
    parsed_tafb = parse_duration(collated.trip_footer.data["tafb"])
    if expanded_tafb != parsed_tafb:
        msg = f"Expanded TAFB does not match parsed TAFB for trip. {expanded_tafb=!s} {parsed_tafb=!r}"
        expanded.errors.append(msg)
