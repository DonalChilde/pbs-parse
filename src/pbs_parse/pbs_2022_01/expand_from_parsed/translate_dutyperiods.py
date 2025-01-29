"""FILE: translate_dutyperiods.py."""

import logging
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from pbs_parse.common.get_airport_info import get_airport_info_from_iata
from pbs_parse.common.parse_duration import parse_duration
from pbs_parse.pbs_2022_01.expand_from_parsed.next_utc import next_utc
from pbs_parse.pbs_2022_01.expand_from_parsed.report_to_first_flight_delta import (
    report_to_first_flight_delta,
)
from pbs_parse.pbs_2022_01.expand_from_parsed.state import State
from pbs_parse.pbs_2022_01.expand_from_parsed.translate_flights import translate_flights
from pbs_parse.pbs_2022_01.expand_from_parsed.translate_layover import translate_layover
from pbs_parse.pbs_2022_01.expand_from_parsed.utc_to_local import utc_to_local
from pbs_parse.pbs_2022_01.models.collated_trip import CollatedDutyPeriod
from pbs_parse.pbs_2022_01.models.expanded import DutyPeriod

UTC = ZoneInfo("UTC")
logger = logging.getLogger(__name__)


def translate_dutyperiods(
    collated_dutyperiods: list[CollatedDutyPeriod],
    start_date: date,
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
    report_utc = assemble_first_report_utc(
        collated_dutyperiods=collated_dutyperiods, start_date=start_date, state=state
    )
    for idx, collated_dp in enumerate(collated_dutyperiods, start=1):
        state.dp_idx = idx
        logger.debug(
            "Translating dutyperiod %d with report_utc %s",
            state.dp_idx,
            report_utc.isoformat(),
        )
        expanded_dp = translate_dutyperiod(
            report_utc=report_utc,
            collated_dp=collated_dp,
            state=state,
        )
        expanded_dutyperiods.append(expanded_dp)
        if expanded_dp.layover is not None:
            report_utc = next_utc(
                utc_datetime=expanded_dp.release_utc, delta=expanded_dp.layover.rest
            )
    return expanded_dutyperiods


def translate_dutyperiod(
    report_utc: datetime,
    collated_dp: CollatedDutyPeriod,
    state: State,
) -> DutyPeriod:
    """translate_dutyperiod.

    Args:
        report_utc (datetime): _description_
        next_report_lcl (str): _description_
        collated_dp (CollatedDutyPeriod): _description_
        state (State): _description_

    Returns:
        DutyPeriod: _description_
    """
    report_station = get_airport_info_from_iata(
        iata=collated_dp.flights[0].data["departure_station"]
    )
    release_station = get_airport_info_from_iata(
        collated_dp.flights[-1].data["arrival_station"]
    )
    duty = parse_duration(collated_dp.release.data["duty"])
    release_utc = next_utc(utc_datetime=report_utc, delta=duty)
    flight_duty = parse_duration(collated_dp.release.data["flight_duty"])
    operating_time = parse_duration(collated_dp.release.data["block"])
    soft_time = parse_duration(collated_dp.release.data["synth"])
    first_departure_delta = report_to_first_flight_delta(collated_dp=collated_dp)
    first_departure_utc = next_utc(utc_datetime=report_utc, delta=first_departure_delta)
    flights = translate_flights(
        first_departure_utc=first_departure_utc,
        parsed_flights=collated_dp.flights,
        state=state,
    )
    layover = translate_layover(
        dutyperiod_release_utc=release_utc,
        layover=collated_dp.layover,
        hotel_info=collated_dp.hotel,
        state=state,
    )
    flight_time = timedelta(
        seconds=sum([x.flight_time.total_seconds() for x in flights])
    )
    report_lcl_tzinfo = ZoneInfo(report_station.tz_name)
    report_lcl = utc_to_local(
        report_utc, report_lcl_tzinfo, collated_dp.report.data["report"]["lcl"]
    )
    expanded_dutyperiod = DutyPeriod(
        report_station=report_station,
        report_utc=report_utc,
        report_lcl=report_lcl,
        report_hbt=report_utc.astimezone(state.hbt_tzinfo),
        release_station=release_station,
        release_utc=release_utc,
        release_lcl=release_utc.astimezone(ZoneInfo(release_station.tz_name)),
        release_hbt=release_utc.astimezone(state.hbt_tzinfo),
        flights=flights,
        duty=duty,
        flight_duty=flight_duty,
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        layover=layover,
    )
    return expanded_dutyperiod


def assemble_first_report_utc(
    collated_dutyperiods: list[CollatedDutyPeriod], start_date: date, state: State
) -> datetime:
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
    first_dep = time.fromisoformat(
        collated_dutyperiods[0].flights[0].data["departure_time"]["lcl"]
    )
    first_dep_utc = datetime.combine(
        start_date, first_dep, state.hbt_tzinfo
    ).astimezone(UTC)
    first_report_utc = first_dep_utc - report_to_first_flight_delta(
        collated_dp=collated_dutyperiods[0]
    )
    return first_report_utc
