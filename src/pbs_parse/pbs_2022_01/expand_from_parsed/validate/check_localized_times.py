"""FILE: check_localized_times.py."""

from pfmsoft.state_parser.model import ParsedIndexedString
from whenever import ZonedDateTime

from pbs_parse.common.parse_time_whenever import parse_time
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
                hb_tz_name=expanded.start_station.tz_name,
            )
            expanded.errors.extend(flt_errors)
    trip_errors = trip_report_release(expanded=expanded, collated=collated)
    expanded.errors.extend(trip_errors)


def test_time(zdt: ZonedDateTime, time_string: str, tz: str, ctx: str) -> str:
    """test_time.

    Args:
        zdt (ZonedDateTime): _description_
        time_string (str): _description_
        tz (str): _description_
        ctx (dict[str, str]): _description_

    Returns:
        str: _description_
    """
    parsed_time = parse_time(time_string)
    localized_dt = zdt.to_tz(tz)
    if parsed_time != localized_dt.time():
        return (
            f"{ctx=} "
            f"{zdt.format_common_iso()} when localized to "
            f"{localized_dt.format_common_iso()} time does not match "
            f"{time_string=} {parsed_time=!r} {tz=}"
        )
    return ""


def dutyperiod_times(
    expanded_dp: DutyPeriod,
    collated_dp: CollatedDutyPeriod,
    dp_idx: int,
    hb_tz_name: str,
) -> list[str]:
    """Check the dutyperiod report and release times."""
    errors: list[str] = []
    if error := test_time(
        zdt=expanded_dp.report,
        time_string=collated_dp.report.data["report"]["lcl"],
        tz=expanded_dp.report_station.tz_name,
        ctx=f"{dp_idx=} report_local",
    ):
        errors.append(error)
    if error := test_time(
        zdt=expanded_dp.report,
        time_string=collated_dp.report.data["report"]["hbt"],
        tz=hb_tz_name,
        ctx=f"{dp_idx=} report_hbt",
    ):
        errors.append(error)
    if error := test_time(
        zdt=expanded_dp.release,
        time_string=collated_dp.release.data["release"]["lcl"],
        tz=expanded_dp.release_station.tz_name,
        ctx=f"{dp_idx=} release_local",
    ):
        errors.append(error)
    if error := test_time(
        zdt=expanded_dp.release,
        time_string=collated_dp.release.data["release"]["hbt"],
        tz=hb_tz_name,
        ctx=f"{dp_idx=} release_hbt",
    ):
        errors.append(error)

    return errors


def flight_times(
    e_flight: Flight,
    collated_flight: ParsedIndexedString,
    hb_tz_name: str,
    dp_idx: int,
    flt_idx: int,
) -> list[str]:
    """Check the flight departure and arrival times."""
    errors: list[str] = []
    if error := test_time(
        zdt=e_flight.departure,
        time_string=collated_flight.data["departure_time"]["lcl"],
        tz=e_flight.departure_station.tz_name,
        ctx=f"{dp_idx=} {flt_idx=} departure_lcl",
    ):
        errors.append(error)
    if error := test_time(
        zdt=e_flight.departure,
        time_string=collated_flight.data["departure_time"]["hbt"],
        tz=hb_tz_name,
        ctx=f"{dp_idx=} {flt_idx=} departure_hbt",
    ):
        errors.append(error)
    if error := test_time(
        zdt=e_flight.arrival,
        time_string=collated_flight.data["arrival_time"]["lcl"],
        tz=e_flight.arrival_station.tz_name,
        ctx=f"{dp_idx=} {flt_idx=} arrival_lcl",
    ):
        errors.append(error)
    if error := test_time(
        zdt=e_flight.arrival,
        time_string=collated_flight.data["arrival_time"]["hbt"],
        tz=hb_tz_name,
        ctx=f"{dp_idx=} {flt_idx=} arrival_hbt",
    ):
        errors.append(error)
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
    if error := test_time(
        zdt=expanded.start,
        time_string=collated.dutyperiods[0].report.data["report"]["lcl"],
        tz=expanded.start_station.tz_name,
        ctx="trip_start_lcl",
    ):
        errors.append(error)
    if error := test_time(
        zdt=expanded.start,
        time_string=collated.dutyperiods[0].report.data["report"]["hbt"],
        tz=expanded.start_station.tz_name,
        ctx="trip_start_hbt",
    ):
        errors.append(error)
    if error := test_time(
        zdt=expanded.end,
        time_string=collated.dutyperiods[-1].release.data["release"]["lcl"],
        tz=expanded.end_station.tz_name,
        ctx="trip_end_lcl",
    ):
        errors.append(error)
    if error := test_time(
        zdt=expanded.end,
        time_string=collated.dutyperiods[-1].release.data["release"]["hbt"],
        tz=expanded.end_station.tz_name,
        ctx="trip_end_hbt",
    ):
        errors.append(error)

    return errors
