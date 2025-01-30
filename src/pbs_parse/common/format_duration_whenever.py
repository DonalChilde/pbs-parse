"""FILE: format_duration_whenever.py."""

"""FILE: format_duration.py."""


from whenever import TimeDelta


def format_td(td: TimeDelta) -> str:
    """format_td.

    Args:
        td (timedelta): _description_

    Returns:
        str: _description_
    """
    factored = td.in_hrs_mins_secs_nanos()
    return f"{factored[0]}.{factored[1]:02n}"
