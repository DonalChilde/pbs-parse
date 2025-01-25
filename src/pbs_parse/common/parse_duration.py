"""FILE: parse_duration.py."""

from datetime import timedelta

from pbs_parse.snippets.datetime.duration_regex import pattern_HHHMM

DURATION_REGEX = pattern_HHHMM(".")


def parse_duration(duration_string: str) -> timedelta:
    """parse_duration.

    Args:
        duration_string (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        timedelta: _description_
    """
    match = DURATION_REGEX.fullmatch(duration_string)
    if match is None:
        raise ValueError(
            f"No match found for {duration_string} does it match the pattern HHH.MM?"
        )
    data = match.groupdict()
    hours = int(data["hours"])
    minutes = int(data["minutes"])
    return timedelta(hours=hours, minutes=minutes)
