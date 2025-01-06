"""Validate expanded trips."""

import logging

from pbs_parse.pbs_2022_01.models import expanded as ET
from pbs_parse.pbs_2022_01.models import structured as ST
from pbs_parse.pbs_2022_01.models.expanded_validation import ExpandedValidation

logger = logging.getLogger(__name__)


class ExpandedValidator:
    """_summary_."""

    def validate(self, validation_model: ExpandedValidation):
        """validate.

        Args:
            validation_model (ExpandedValidation): _description_
        """
        validate_expanded(validation_model=validation_model)


def validate_expanded(validation_model: ExpandedValidation):
    """validate.

    Args:
        validation_model (ExpandedValidation): _description_
    """
    _validate(validation_model=validation_model)


def _validate(validation_model: ExpandedValidation) -> None:
    """Validator functions called from here."""
    _check_localized_times(validation_model=validation_model)
    return None


def _check_localized_times(validation_model: ExpandedValidation) -> None:
    """Check that the localized utc times match the structured trip times."""
    hb_tz_name = validation_model.expanded.base_equipment.base.tz_name
    for dp_idx, dutyperiods in enumerate(
        zip(
            validation_model.expanded.dutyperiods,
            validation_model.structured.dutyperiods,
            strict=True,
        ),
        start=1,
    ):
        e_dutyperiod, s_dutyperiod = dutyperiods
        dp_errors = _check_dutyperiod_times(
            e_dutyperiod=e_dutyperiod,
            s_dutyperiod=s_dutyperiod,
            hb_tz_name=hb_tz_name,
            dp_idx=dp_idx,
        )
        if dp_errors:
            validation_model.errors.extend(dp_errors)
        for flt_idx, flights in enumerate(
            zip(dutyperiods[0].flights, dutyperiods[1].flights, strict=True), start=1
        ):
            e_flight, s_flight = flights
            flt_errors = _check_flight_times(
                e_flight=e_flight,
                s_flight=s_flight,
                hb_tz_name=hb_tz_name,
                dp_idx=dp_idx,
                flt_idx=flt_idx,
            )
            validation_model.errors.extend(flt_errors)
    trip_errors = _check_trip_report_release(
        e_trip=validation_model.expanded, s_trip=validation_model.structured
    )
    validation_model.errors.extend(trip_errors)


def _check_dutyperiod_times(
    e_dutyperiod: ET.DutyPeriod,
    s_dutyperiod: ST.DutyPeriod,
    hb_tz_name: str,
    dp_idx: int,
) -> list[str]:
    """Check the dutyperiod report and release times."""
    errors: list[str] = []
    tests = [
        (e_dutyperiod.report_lcl, s_dutyperiod.report_time.lcl, "local report"),
        (e_dutyperiod.report_hbt, s_dutyperiod.report_time.hbt, "hbt report"),
        (e_dutyperiod.release_lcl, s_dutyperiod.release_time.lcl, "local release"),
        (e_dutyperiod.release_hbt, s_dutyperiod.release_time.hbt, "hbt release"),
    ]
    for test in tests:
        if test[0].strftime("%H%M") != test[1]:
            errors.append(
                f"Expanded {test[0].isoformat()} time {test[0].time()} does not match Structured {test[1]}"
                f" for dutyperiod idx {dp_idx}, field `{test[2]}` "
            )

    return errors


def _check_flight_times(
    e_flight: ET.Flight, s_flight: ST.Flight, hb_tz_name: str, dp_idx: int, flt_idx: int
) -> list[str]:
    """Check the flight departure and arrival times."""
    errors: list[str] = []
    tests = [
        (e_flight.departure_lcl, s_flight.departure_time.lcl, "local departure"),
        (e_flight.departure_hbt, s_flight.departure_time.hbt, "hbt departure"),
        (e_flight.arrival_lcl, s_flight.arrival_time.lcl, "local arrival"),
        (e_flight.arrival_hbt, s_flight.arrival_time.hbt, "hbt arrival"),
    ]

    for test in tests:
        if test[0].strftime("%H%M") != test[1]:
            errors.append(
                f"Expanded {test[0].isoformat()} time {test[0].time()} does not match Structured "
                f"{test[1]} for dutyperiod-{dp_idx} flight-{flt_idx} field `{test[2]}`"
            )
    return errors


def _check_trip_report_release(
    e_trip: ET.ExpandedTrip, s_trip: ST.StructuredTrip
) -> list[str]:
    errors: list[str] = []
    tests = [
        (e_trip.start_lcl, s_trip.dutyperiods[0].report_time.lcl, "local start"),
        (e_trip.start_hbt, s_trip.dutyperiods[0].report_time.hbt, "hbt start"),
        (e_trip.end_lcl, s_trip.dutyperiods[-1].release_time.lcl, "local end"),
        (e_trip.end_hbt, s_trip.dutyperiods[-1].release_time.lcl, "hbt arrival"),
    ]
    for test in tests:
        if test[0].strftime("%H%M") != test[1]:
            errors.append(
                f"Expanded {test[0].isoformat()} time {test[0].time()} does not match Structured "
                f"{test[1]} for trip {s_trip.number} field `{test[2]}`"
            )
    return errors
