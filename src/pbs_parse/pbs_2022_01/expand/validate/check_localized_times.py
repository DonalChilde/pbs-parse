"""FILE: check_localized_times.py."""

from datetime import datetime

from pbs_parse.pbs_2022_01.models import expanded as ET
from pbs_parse.pbs_2022_01.models import structured as ST
from pbs_parse.pbs_2022_01.models.expanded_validation import ExpandedValidation


def check_localized_times(vm: ExpandedValidation) -> None:
    """Check that the localized utc times match the structured trip times."""
    for dp_idx, dutyperiods in enumerate(
        zip(vm.expanded.dutyperiods, vm.structured.dutyperiods, strict=True),
        start=1,
    ):
        e_dutyperiod, s_dutyperiod = dutyperiods
        dp_errors = dutyperiod_times(
            e_dutyperiod=e_dutyperiod,
            s_dutyperiod=s_dutyperiod,
            dp_idx=dp_idx,
            hb_tz_name=vm.expanded.start_station.tz_name,
        )
        if dp_errors:
            vm.expanded.errors.extend(dp_errors)
        for flt_idx, flights in enumerate(
            zip(dutyperiods[0].flights, dutyperiods[1].flights, strict=True), start=1
        ):
            e_flight, s_flight = flights
            flt_errors = flight_times(
                e_flight=e_flight,
                s_flight=s_flight,
                dp_idx=dp_idx,
                flt_idx=flt_idx,
            )
            vm.expanded.errors.extend(flt_errors)
    trip_errors = trip_report_release(e_trip=vm.expanded, s_trip=vm.structured)
    vm.expanded.errors.extend(trip_errors)


def dutyperiod_times(
    e_dutyperiod: ET.DutyPeriod,
    s_dutyperiod: ST.DutyPeriod,
    dp_idx: int,
    hb_tz_name: str,
) -> list[str]:
    """Check the dutyperiod report and release times."""
    errors: list[str] = []

    tests = [
        (
            e_dutyperiod.report_lcl,
            s_dutyperiod.report_time.lcl,
            "local report",
            e_dutyperiod.report_station.tz_name,
            e_dutyperiod.report_utc,
        ),
        (
            e_dutyperiod.report_hbt,
            s_dutyperiod.report_time.hbt,
            "hbt report",
            hb_tz_name,
            e_dutyperiod.report_utc,
        ),
        (
            e_dutyperiod.release_lcl,
            s_dutyperiod.release_time.lcl,
            "local release",
            e_dutyperiod.release_station.tz_name,
            e_dutyperiod.release_utc,
        ),
        (
            e_dutyperiod.release_hbt,
            s_dutyperiod.release_time.hbt,
            "hbt release",
            hb_tz_name,
            e_dutyperiod.release_utc,
        ),
    ]
    for test in tests:
        if test[0].strftime("%H%M") != test[1]:
            errors.append(
                f"Expanded {test[0].isoformat()} time {test[0].time()} does not match Structured {test[1]}"
                f" for dutyperiod-{dp_idx}, field `{test[2]}`, tz_name={test[3]}, utc={test[4]} "
            )

    return errors


def flight_times(
    e_flight: ET.Flight, s_flight: ST.Flight, dp_idx: int, flt_idx: int
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


def trip_report_release(
    e_trip: ET.ExpandedTrip, s_trip: ST.StructuredTrip
) -> list[str]:
    """trip_report_release.

    Args:
        e_trip (ET.ExpandedTrip): _description_
        s_trip (ST.StructuredTrip): _description_

    Returns:
        list[str]: _description_
    """
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
