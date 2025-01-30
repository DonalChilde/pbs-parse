"""FILE: translate_dutyperiods.py."""

import logging
from zoneinfo import ZoneInfo

from whenever import Date, TimeDelta, ZonedDateTime

from pbs_parse.common.get_airport_info import get_airport_info_from_iata
from pbs_parse.common.parse_duration_whenever import parse_duration
from pbs_parse.common.parse_time_whenever import parse_time
from pbs_parse.pbs_2022_01.expand_from_parsed.report_to_first_flight_delta import (
    report_to_first_flight_delta,
)
from pbs_parse.pbs_2022_01.expand_from_parsed.state import State
from pbs_parse.pbs_2022_01.expand_from_parsed.translate_flights import translate_flights
from pbs_parse.pbs_2022_01.expand_from_parsed.translate_layover import translate_layover
from pbs_parse.pbs_2022_01.models.collated_trip import CollatedDutyPeriod
from pbs_parse.pbs_2022_01.models.expanded import DutyPeriod

UTC = ZoneInfo("UTC")
logger = logging.getLogger(__name__)


def translate_dutyperiods(
    collated_dutyperiods: list[CollatedDutyPeriod],
    start_date: Date,
    state: State,
) -> list[DutyPeriod]:
    """translate_dutyperiods.

    Args:
        collated_dutyperiods (list[CollatedDutyPeriod]): _description_
        start_date (date): _description_
        state (State): _description_

    Returns:
        list[DutyPeriod]: _description_
    """
    expanded_dutyperiods: list[DutyPeriod] = []
    report = assemble_first_report(
        collated_dutyperiods=collated_dutyperiods, start_date=start_date, state=state
    )
    for idx, collated_dp in enumerate(collated_dutyperiods, start=1):
        state.dp_idx = idx
        logger.debug(
            "Translating dutyperiod %d with report %s",
            state.dp_idx,
            report.format_common_iso(),
        )
        expanded_dp = translate_dutyperiod(
            report=report,
            collated_dp=collated_dp,
            state=state,
        )
        expanded_dutyperiods.append(expanded_dp)
        if expanded_dp.layover is not None:
            report = expanded_dp.release + expanded_dp.layover.rest

    return expanded_dutyperiods


def translate_dutyperiod(
    report: ZonedDateTime,
    collated_dp: CollatedDutyPeriod,
    state: State,
) -> DutyPeriod:
    """translate_dutyperiod.

    Args:
        report (ZonedDateTime): _description_
        collated_dp (CollatedDutyPeriod): _description_
        state (State): _description_

    Returns:
        DutyPeriod: _description_
    """
    report_station = get_airport_info_from_iata(
        iata=collated_dp.flights[0].data["departure_station"]
    )
    if report.tz != report_station.tz_name:
        report = report.to_tz(report_station.tz_name)
    release_station = get_airport_info_from_iata(
        collated_dp.flights[-1].data["arrival_station"]
    )
    duty = parse_duration(collated_dp.release.data["duty"])
    release = (report + duty).to_tz(release_station.tz_name)
    flight_duty = parse_duration(collated_dp.release.data["flight_duty"])
    operating_time = parse_duration(collated_dp.release.data["block"])
    soft_time = parse_duration(collated_dp.release.data["synth"])
    first_departure_delta = report_to_first_flight_delta(collated_dp=collated_dp)
    first_departure = report + first_departure_delta
    flights = translate_flights(
        first_departure=first_departure,
        parsed_flights=collated_dp.flights,
        state=state,
    )
    layover = translate_layover(
        dutyperiod_release=release,
        layover=collated_dp.layover,
        hotel_info=collated_dp.hotel,
        state=state,
    )
    flight_time = TimeDelta(
        nanoseconds=sum([x.flight_time.in_nanoseconds() for x in flights])
    )
    expanded_dutyperiod = DutyPeriod(
        report_station=report_station,
        report=report,
        release_station=release_station,
        release=release,
        flights=flights,
        duty=duty,
        flight_duty=flight_duty,
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        layover=layover,
    )
    return expanded_dutyperiod


def assemble_first_report(
    collated_dutyperiods: list[CollatedDutyPeriod], start_date: Date, state: State
) -> ZonedDateTime:
    """assemble_first_report_utc.

    As of 2024-01-29, AA trip start dates are based on first departure, not report time.
    The start date for trips whose report/first departure time overlap 00:00 will have
    to have report date adjusted.

    Args:
        collated_dutyperiods (list[CollatedDutyPeriod]): _description_
        start_date (date): _description_
        state (State): _description_

    Returns:
        datetime: _description_
    """
    departure_time = parse_time(
        collated_dutyperiods[0].flights[0].data["departure_time"]["lcl"]
    )
    departure_station = get_airport_info_from_iata(
        collated_dutyperiods[0].flights[0].data["departure_station"]
    )
    first_departure = ZonedDateTime(
        start_date.year,
        start_date.month,
        start_date.day,
        departure_time.hour,
        departure_time.minute,
        departure_time.second,
        tz=departure_station.tz_name,
    )
    first_report_utc = first_departure - report_to_first_flight_delta(
        collated_dp=collated_dutyperiods[0]
    )
    return first_report_utc
