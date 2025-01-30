"""FILE: parse_time_whenever.py."""

from whenever import Time


def parse_time(value: str) -> Time:
    """Parse a time represented by HHMM."""
    if len(value) != 4:
        raise ValueError(f"Expected to parse a time with four characters, got {value=}")
    hours = value[:2]
    minutes = value[2:]
    return Time(hour=int(hours), minute=int(minutes))
