"""Validate structured trips."""

import logging
from datetime import date
from pathlib import Path

from pbs_parse.pbs_2022_01.models import parsed_trip as PT
from pbs_parse.pbs_2022_01.models import structured as ST
from pbs_parse.pbs_2022_01.models.validation import Context
from pbs_parse.snippets.datetime.date_range import date_range

logger = logging.getLogger(__name__)

# TODO this needs work on context object and interface.


def validate(
    parsed_trip: PT.ParsedTrip,
    structured_trip: ST.StructuredTrip,
    ctx: Context | None = None,
) -> Context:
    """Validate a StructuredTrip.

    Args:
        parsed_trip (PT.ParsedTrip): The ParsedTrip used to create the StructuredTrip.
        structured_trip (ST.StructuredTrip): The StructuredTrip.
        ctx (Context | None, optional): An object used to pass information useful for validation. Defaults to None.

    Returns:
        Context: _description_
    """
    if ctx is None:
        ctx = Context(parsed_trip=parsed_trip, structured_trip=structured_trip)
    ctx.external_start_dates = _possible_start_dates(structured_trip=structured_trip)
    _validate(ctx=ctx)
    return ctx


def validate_files(parsed_trip_path: Path, structured_trip_path: Path) -> Context:
    """Validate_files _summary_.

    Returns:
        _type_: _description_
    """
    parsed_trip = PT.PARSED_TRIP_SERIALIZER.load_from_json(path_in=parsed_trip_path)
    structured_trip = ST.STRUCTURED_TRIP_SERIALIZER.load_from_json(
        path_in=structured_trip_path
    )

    ctx = Context(
        parsed_trip=parsed_trip,
        structured_trip=structured_trip,
        parsed_path=str(parsed_trip_path),
        structured_path=str(structured_trip_path),
    )
    ctx.external_start_dates = _possible_start_dates(structured_trip=structured_trip)
    _validate(ctx=ctx)
    return ctx


def _possible_start_dates(structured_trip: ST.StructuredTrip) -> list[date]:
    try:
        start_date = date.fromisoformat(structured_trip.external.effective_from)
        end_date = date.fromisoformat(structured_trip.external.effective_to)
        start_dates = list(date_range(start_date=start_date, end_date=end_date))
    except ValueError as e:
        logger.exception(
            msg=f"Unable to form date range using {structured_trip.external!r} {e}",
        )
        return []
    return start_dates


def _validate(ctx: Context) -> None:
    _calendar_starts_count(ctx=ctx)
    return None


def _calendar_starts_count(ctx: Context) -> None:
    """Check if whole calendar was captured."""
    if len(ctx.structured_trip.calendar) != len(ctx.external_start_dates):
        msg = (
            f"len(ctx.structured_trip.calendar) != len(ctx.external_start_dates)\n"
            f"\t{len(ctx.structured_trip.calendar)} != {len(ctx.external_start_dates)}\n"
            f"\tctx.structured_trip.calendar -> {ctx.structured_trip.calendar!r}\n"
            f"\tctx.external_start_dates -> {ctx.external_start_dates}\n"
        )
        ctx.errors.append(msg)
