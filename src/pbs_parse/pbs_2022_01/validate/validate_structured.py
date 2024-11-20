import logging
from datetime import date, timedelta
from pathlib import Path
from typing import Iterator, Optional

from pbs_parse.pbs_2022_01.models import parsed_trip as PT
from pbs_parse.pbs_2022_01.models import structured as ST
from pbs_parse.pbs_2022_01.models.validation import Context

logger = logging.getLogger(__name__)


def validate(
    parsed_trip: PT.ParsedTrip,
    structured_trip: ST.StructuredTrip,
    ctx: Optional[Context] = None,
) -> Context:
    if ctx is None:
        ctx = Context(parsed_trip=parsed_trip, structured_trip=structured_trip)
    ctx.external_start_dates = _get_list_of_start_dates(structured_trip=structured_trip)
    _validate(ctx=ctx)
    return ctx


def validate_files(parsed_trip_path: Path, structured_trip_path: Path) -> Context:
    parsed_serializer = PT.parsed_trip_serializer()
    structured_serializer = ST.structured_trip_serializer()
    parsed_trip = parsed_serializer.load_from_json(path_in=parsed_trip_path)
    structured_trip = structured_serializer.load_from_json(path_in=structured_trip_path)
    ctx = Context(
        parsed_trip=parsed_trip,
        structured_trip=structured_trip,
        parsed_path=str(parsed_trip_path),
        structured_path=str(structured_trip_path),
    )
    ctx.external_start_dates = _get_list_of_start_dates(structured_trip=structured_trip)
    _validate(ctx=ctx)
    return ctx


def _get_list_of_start_dates(structured_trip: ST.StructuredTrip) -> list[date]:
    try:
        start_date = date.fromisoformat(structured_trip.external.effective_from)
        end_date = date.fromisoformat(structured_trip.external.effective_to)
        start_dates = list(dates_range(start_date=start_date, end_date=end_date))
    except ValueError as e:
        logger.exception(
            msg=f"Unable to form date range using {structured_trip.external!r} {e}",
        )
        return []
    return start_dates


def dates_range(start_date: date, end_date: date) -> Iterator[date]:
    """A generator for dates between start and end, inclusive.

    start is assumed to come before end, chronologically.
    """
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date = current_date + timedelta(days=1)


def _validate(ctx: Context) -> None:
    _calendar_starts_count(ctx=ctx)
    return None


def _calendar_starts_count(ctx: Context) -> None:
    if len(ctx.structured_trip.calendar) != len(ctx.external_start_dates):
        msg = (
            f"len(ctx.structured_trip.calendar) != len(ctx.external_start_dates)\n"
            f"\t{len(ctx.structured_trip.calendar)} != {len(ctx.external_start_dates)}\n"
            f"\tctx.structured_trip.calendar -> {ctx.structured_trip.calendar!r}\n"
            f"\tctx.external_start_dates -> {ctx.external_start_dates}\n"
        )
        ctx.errors.append(msg)
