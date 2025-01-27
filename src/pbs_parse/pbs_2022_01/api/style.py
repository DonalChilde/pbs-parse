"""FILE: style.py."""

from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip


def expanded_debug(parsed: ParsedTrip, expanded: ExpandedTrip) -> str:
    """expanded_debug.

    Args:
        parsed (ParsedTrip): _description_
        expanded (ExpandedTrip): _description_

    Returns:
        str: _description_
    """
    return f"{parsed!s}\n{expanded!s}\n"
