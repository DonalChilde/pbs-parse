"""Validate expanded trips."""

import logging
from pathlib import Path

from pbs_parse.pbs_2022_01.models import expanded as ET
from pbs_parse.pbs_2022_01.models import structured as ST
from pbs_parse.pbs_2022_01.models.structured_validation import ExpandedValidation

logger = logging.getLogger(__name__)


def validate(ctx: ExpandedValidation) -> ExpandedValidation:
    """validate.

    Args:
        ctx (ExpandedValidation): _description_

    Returns:
        ExpandedValidation: Will contain any error messages generated.
    """
    _validate(ctx=ctx)
    return ctx


def validate_files(
    expanded_trip_path: Path, structured_trip_path: Path
) -> ExpandedValidation:
    """Validate_files _summary_.

    Returns:
        StructuredValidation: Will contain any error messages generated.
    """
    expanded_trip = ET.EXPANDED_TRIP_SERIALIZER.load_from_json(
        path_in=expanded_trip_path
    )
    structured_trip = ST.STRUCTURED_TRIP_SERIALIZER.load_from_json(
        path_in=structured_trip_path
    )

    ctx = ExpandedValidation(
        expanded_trip=expanded_trip,
        structured_trip=structured_trip,
        expanded_path=str(expanded_trip_path),
        structured_path=str(structured_trip_path),
    )
    _validate(ctx=ctx)
    return ctx


def _validate(ctx: ExpandedValidation) -> None:
    """Validator functions called from here."""
    _check_localized_times(ctx=ctx)
    return None


def _check_localized_times(ctx: ExpandedValidation) -> None:
    """Check that the localized utc times match the structured trip times."""
    hb_tz_name = ctx.expanded_trip.base_equipment.base.tz_name
    for dp_idx, dutyperiods in enumerate(
        zip(
            ctx.expanded_trip.dutyperiods, ctx.structured_trip.dutyperiods, strict=True
        ),
        start=1,
    ):
        dp_errors = _check_dutyperiod_times(
            values=dutyperiods, hb_tz_name=hb_tz_name, dp_idx=dp_idx
        )
        ctx.errors.extend(dp_errors)
        for flt_idx, flights in enumerate(
            zip(dutyperiods[0].flights, dutyperiods[1].flights, strict=True), start=1
        ):
            flt_errors = _check_flight_times(
                values=flights, hb_tz_name=hb_tz_name, dp_idx=dp_idx, flt_idx=flt_idx
            )
            ctx.errors.extend(flt_errors)


def _check_dutyperiod_times(
    values: tuple[ET.DutyPeriod, ST.DutyPeriod], hb_tz_name: str, dp_idx: int
) -> list[str]:
    """Check the dutyperiod report and release times."""
    errors: list[str] = []
    tests = [
        (values[0].report_lcl, values[1].report_time.lcl, "local report"),
        # (values[0].report_hbt, values[1].report_time.hbt, "hbt report"),
        (values[0].release_lcl, values[1].release_time.lcl, "local release"),
        # (values[0].release_hbt, values[1].release_time.hbt, "hbt release"),
    ]
    for test in tests:
        if test[0].strftime("%H%M") != test[1]:
            errors.append(
                f"Expanded {test[0].isoformat()} time does not match Structured {test[1]}"
                f" for dutyperiod idx {dp_idx}, field `{test[2]}`"
            )

    return errors


def _check_flight_times(
    values: tuple[ET.Flight, ST.Flight], hb_tz_name: str, dp_idx: int, flt_idx: int
) -> list[str]:
    """Check the flight departure and arrival times."""
    errors: list[str] = []
    tests = [
        (values[0].departure_lcl, values[1].departure_time.lcl, "local departure"),
        # (values[0].departure_hbt, values[1].departure_time.hbt, "hbt departure"),
        (values[0].arrival_lcl, values[1].arrival_time.lcl, "local arrival"),
        # (values[0].arrival_hbt, values[1].arrival_time.hbt, "hbt arrival"),
    ]

    for test in tests:
        if test[0].strftime("%H%M") != test[1]:
            errors.append(
                f"Expanded {test[0].isoformat()} time does not match Structured "
                f"{test[1]} for dutyperiod-{dp_idx} flight-{flt_idx} field `{test[2]}`"
            )

    return errors
