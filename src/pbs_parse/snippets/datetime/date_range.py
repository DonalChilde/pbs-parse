"""Get a range of dates."""

from collections.abc import Iterator
from datetime import date, datetime


def date_range(
    start_date: date | datetime,
    end_date: date | datetime,
    inclusive: bool = True,
) -> Iterator[date]:
    """Generate dates between a start and end date.

    Will work with ascending or descending dates. Will include end date in
    results by default.

    from: https://stackoverflow.com/a/32616832/105844
    """
    start_ordinal = start_date.toordinal()
    end_ordinal = end_date.toordinal()
    extra = 0
    step = 1
    if inclusive:
        extra = 1

    if start_ordinal > end_ordinal:
        step = -1
        extra = extra * -1

    for ordinal in range(start_ordinal, end_ordinal + extra, step):
        yield date.fromordinal(ordinal)
