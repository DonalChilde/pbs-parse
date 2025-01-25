"""FILE: build_start_dates.py."""

from datetime import date

from pbs_parse.snippets.datetime.date_range import date_range


def build_start_dates(
    effective_from: date, effective_to: date, calendar: list[str]
) -> list[date]:
    """build_start_dates.

    Args:
        effective_from (date): _description_
        effective_to (date): _description_
        calendar (list[str]): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        list[date]: _description_
    """
    effective_dates = list(date_range(start_date=effective_from, end_date=effective_to))
    if len(effective_dates) != len(calendar):
        raise ValueError(
            f"The length of effective_dates {effective_dates!r} does not match the length of calendar {calendar!r}"
        )
    result: list[date] = []
    for idx, item in enumerate(calendar):
        if item.isnumeric():
            if effective_dates[idx].day != int(item):
                raise ValueError(
                    f"Calendar item {item} does not have the same day as {effective_dates[idx]}"
                )
            result.append(effective_dates[idx])
    return result
