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
    return f"Text Input:\n{parsed.original_text(with_line_num=False)!s}\n{expanded!s}\n{parsed!s}"
