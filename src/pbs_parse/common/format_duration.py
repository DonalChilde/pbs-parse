"""FILE: format_duration.py."""

from datetime import timedelta

from pbs_parse.snippets.datetime.factored_timedelta import factor_time_delta


def format_td(td: timedelta) -> str:
    """format_td.

    Args:
        td (timedelta): _description_

    Returns:
        str: _description_
    """
    factored = factor_time_delta(td=td)
    hours = (factored.days * 24) + factored.hours
    minutes = factored.minutes
    return f"{hours}.{minutes:02n}"
