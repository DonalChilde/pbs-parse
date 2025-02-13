"""FILE: build_start_dates.py."""

from whenever import Date

from pbs_parse.snippets.datetime.date_range import date_range


def build_start_dates(
    effective_from: Date, effective_to: Date, calendar: list[str]
) -> list[Date]:
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
    # Get a range of py dates to convert to whenever dates, waiting for whenever to implement date range.
    py_dates = date_range(
        start_date=effective_from.py_date(), end_date=effective_to.py_date()
    )
    effective_dates = [Date.from_py_date(x) for x in py_dates]
    if len(effective_dates) != len(calendar):
        raise ValueError(
            f"The len(effective_dates)={len(effective_dates)} {effective_dates!r} does "
            f"not match len(calendar)={len(calendar)} of calendar {calendar!r} locals={locals()!r}"
        )
    result: list[Date] = []
    for idx, item in enumerate(calendar):
        if item.isnumeric():
            if effective_dates[idx].day != int(item):
                raise ValueError(
                    f"Calendar item {item} does not have the same day as {effective_dates[idx]} locals={locals()!r}"
                )
            result.append(effective_dates[idx])
    return result
