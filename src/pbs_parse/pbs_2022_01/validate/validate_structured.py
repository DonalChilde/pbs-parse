"""Validate structured trips."""

import logging
from datetime import date
from pathlib import Path

from pbs_parse.pbs_2022_01.models import parsed_trip as PT
from pbs_parse.pbs_2022_01.models import structured as ST
from pbs_parse.pbs_2022_01.models.structured_validation import StructuredValidation
from pbs_parse.snippets.datetime.date_range import date_range

logger = logging.getLogger(__name__)


def validate_structured_trip(
    validation_model: StructuredValidation,
) -> StructuredValidation:
    """validate.

    Args:
        validation_model (StructuredValidation): _description_

    Returns:
        StructuredValidation: Will contain any error messages generated.
    """
    validation_model.valid_start_dates = _possible_start_dates(
        structured_trip=validation_model.structured
    )
    _validate(ctx=validation_model)
    return validation_model


def validate_structured_trip_from_file(
    parsed_trip_path: Path, structured_trip_path: Path
) -> StructuredValidation:
    """Validate_files _summary_.

    Returns:
        StructuredValidation: Will contain any error messages generated.
    """
    parsed_trip = PT.PARSED_TRIP_SERIALIZER.load_from_json(path_in=parsed_trip_path)
    structured_trip = ST.STRUCTURED_TRIP_SERIALIZER.load_from_json(
        path_in=structured_trip_path
    )

    ctx = StructuredValidation(
        parsed=parsed_trip,
        structured=structured_trip,
        parsed_path=str(parsed_trip_path),
        structured_path=str(structured_trip_path),
    )
    ctx.valid_start_dates = _possible_start_dates(structured_trip=structured_trip)
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


def _validate(ctx: StructuredValidation) -> None:
    _calendar_starts_count(ctx=ctx)
    return None


def _calendar_starts_count(ctx: StructuredValidation) -> None:
    """Check if whole calendar was captured."""
    if len(ctx.structured.calendar) != len(ctx.valid_start_dates):
        msg = (
            f"len(ctx.structured_trip.calendar) != len(ctx.external_start_dates)\n"
            f"\t{len(ctx.structured.calendar)} != {len(ctx.valid_start_dates)}\n"
            f"\tctx.structured_trip.calendar -> {ctx.structured.calendar!r}\n"
            f"\tctx.external_start_dates -> {ctx.valid_start_dates}\n"
        )
        ctx.errors.append(msg)
