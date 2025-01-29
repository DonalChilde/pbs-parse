"""FILE: check_localized_times.py."""

from pfmsoft.state_parser.model import ParsedIndexedString

from pbs_parse.pbs_2022_01.models.collated_trip import CollatedDutyPeriod, CollatedTrip
from pbs_parse.pbs_2022_01.models.expanded import DutyPeriod, ExpandedTrip, Flight


def check_localized_times(expanded: ExpandedTrip, collated: CollatedTrip) -> None:
    """Check that the localized utc times match the structured trip times."""
    for dp_idx, dutyperiods in enumerate(
        zip(expanded.dutyperiods, collated.dutyperiods, strict=True),
        start=1,
    ):
        expanded_dp, collated_dp = dutyperiods
        dp_errors = dutyperiod_times(
            expanded_dp=expanded_dp,
            collated_dp=collated_dp,
            dp_idx=dp_idx,
            hb_tz_name=expanded.start_station.tz_name,
        )
        if dp_errors:
            expanded.errors.extend(dp_errors)
        for flt_idx, flights in enumerate(
            zip(expanded_dp.flights, collated_dp.flights, strict=True), start=1
        ):
            expanded_flight, collated_flight = flights
            flt_errors = flight_times(
                e_flight=expanded_flight,
                collated_flight=collated_flight,
                dp_idx=dp_idx,
                flt_idx=flt_idx,
            )
            expanded.errors.extend(flt_errors)
    trip_errors = trip_report_release(expanded=expanded, collated=collated)
    expanded.errors.extend(trip_errors)


def dutyperiod_times(
    expanded_dp: DutyPeriod,
    collated_dp: CollatedDutyPeriod,
    dp_idx: int,
    hb_tz_name: str,
) -> list[str]:
    """Check the dutyperiod report and release times."""
    errors: list[str] = []

    tests = [
        (
            expanded_dp.report_lcl,
            collated_dp.report.data["report"]["lcl"],
            "local report",
            expanded_dp.report_station.tz_name,
            expanded_dp.report_utc,
        ),
        (
            expanded_dp.report_hbt,
            collated_dp.report.data["report"]["hbt"],
            "hbt report",
            hb_tz_name,
            expanded_dp.report_utc,
        ),
        (
            expanded_dp.release_lcl,
            collated_dp.release.data["release"]["lcl"],
            "local release",
            expanded_dp.release_station.tz_name,
            expanded_dp.release_utc,
        ),
        (
            expanded_dp.release_hbt,
            collated_dp.release.data["release"]["hbt"],
            "hbt release",
            hb_tz_name,
            expanded_dp.release_utc,
        ),
    ]
    for test in tests:
        if test[0].strftime("%H%M") != test[1]:
            errors.append(
                f"Expanded {test[0].isoformat()} time {test[0].time()} does not match Parsed {test[1]}"
                f" for dutyperiod-{dp_idx}, field `{test[2]}`, tz_name={test[3]}, utc={test[4]} "
            )

    return errors


def flight_times(
    e_flight: Flight, collated_flight: ParsedIndexedString, dp_idx: int, flt_idx: int
) -> list[str]:
    """Check the flight departure and arrival times."""
    errors: list[str] = []
    tests = [
        (
            e_flight.departure_lcl,
            collated_flight.data["departure_time"]["lcl"],
            "local departure",
        ),
        (
            e_flight.departure_hbt,
            collated_flight.data["departure_time"]["hbt"],
            "hbt departure",
        ),
        (
            e_flight.arrival_lcl,
            collated_flight.data["arrival_time"]["lcl"],
            "local arrival",
        ),
        (
            e_flight.arrival_hbt,
            collated_flight.data["arrival_time"]["hbt"],
            "hbt arrival",
        ),
    ]

    for test in tests:
        if test[0].strftime("%H%M") != test[1]:
            errors.append(
                f"Expanded {test[0].isoformat()} time {test[0].time()} does not match Parsed "
                f"{test[1]} for dutyperiod-{dp_idx} flight-{flt_idx} field `{test[2]}`"
            )
    return errors


def trip_report_release(expanded: ExpandedTrip, collated: CollatedTrip) -> list[str]:
    """trip_report_release.

    Args:
        expanded (ExpandedTrip): _description_
        collated (CollatedTrip): _description_

    Returns:
        list[str]: _description_
    """
    errors: list[str] = []
    tests = [
        (
            expanded.start_lcl,
            collated.dutyperiods[0].report.data["report"]["lcl"],
            "local trip start",
        ),
        (
            expanded.start_hbt,
            collated.dutyperiods[0].report.data["report"]["hbt"],
            "hbt trip start",
        ),
        (
            expanded.end_lcl,
            collated.dutyperiods[-1].release.data["release"]["lcl"],
            "local trip end",
        ),
        (
            expanded.end_hbt,
            collated.dutyperiods[-1].release.data["release"]["lcl"],
            "hbt trip end",
        ),
    ]
    for test in tests:
        if test[0].strftime("%H%M") != test[1]:
            errors.append(
                f"Expanded {test[0].isoformat()} time {test[0].time()} does not match Parsed "
                f"{test[1]} for trip {expanded.trip_number} starting at {expanded.start_lcl} field `{test[2]}`"
            )
    return errors
