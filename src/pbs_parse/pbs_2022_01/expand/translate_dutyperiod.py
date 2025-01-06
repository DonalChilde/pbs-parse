"""FILE: translate_dutyperiod.py."""

import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pbs_parse.pbs_2022_01.models.expanded as ET
import pbs_parse.pbs_2022_01.models.structured as ST
from pbs_parse.pbs_2022_01.expand.delta_dt import delta_dt
from pbs_parse.pbs_2022_01.expand.report_to_first_flight_delta import (
    report_to_first_flight_delta,
)
from pbs_parse.pbs_2022_01.expand.state import State
from pbs_parse.pbs_2022_01.expand.translate_flights import translate_flights
from pbs_parse.pbs_2022_01.expand.translate_layover import translate_layover
from pbs_parse.pbs_2022_01.expand.utc_to_local import utc_to_local

logger = logging.getLogger(__name__)


def translate_dutyperiod(
    report_utc: datetime,
    next_report_lcl: str,
    s_dutyperiod: ST.DutyPeriod,
    state: State,
) -> tuple[ET.DutyPeriod, State]:
    """translate_dutyperiod.

    Args:
        report_utc (datetime): _description_
        next_report_lcl (str): _description_
        s_dutyperiod (ST.DutyPeriod): _description_
        state (State): _description_

    Returns:
        tuple[ET.DutyPeriod, State]: _description_
    """
    report_station = ET.get_airport_code_from_iata(
        iata=s_dutyperiod.flights[0].departure_station
    )
    release_station = ET.get_airport_code_from_iata(
        s_dutyperiod.flights[-1].arrival_station
    )
    duty = ST.parse_duration(s_dutyperiod.duty)
    release_utc, state = delta_dt(
        utc_ref=report_utc,
        td=duty,
        lcl_ref=s_dutyperiod.release_time.lcl,
        lcl_tz=release_station.tz_name,
        field_name="release",
        state=state,
    )
    flight_duty = ST.parse_duration(s_dutyperiod.flight_duty)
    operating_time = ST.parse_duration(s_dutyperiod.block)
    soft_time = ST.parse_duration(s_dutyperiod.synth)
    first_departure_delta = report_to_first_flight_delta(s_dutyperiod=s_dutyperiod)
    first_departure_utc, state = delta_dt(
        utc_ref=report_utc,
        td=first_departure_delta,
        lcl_ref=s_dutyperiod.flights[0].departure_time.lcl,
        lcl_tz=report_station.tz_name,
        field_name="First departure",
        state=state,
    )
    flights, state = translate_flights(
        first_departure_utc=first_departure_utc,
        s_flights=s_dutyperiod.flights,
        state=state,
    )
    layover, state = translate_layover(
        dutyperiod_release_utc=release_utc,
        next_report_lcl=next_report_lcl,
        s_layover=s_dutyperiod.layover,
        state=state,
    )
    flight_time = timedelta(
        seconds=sum([x.flight_time.total_seconds() for x in flights])
    )
    report_tzinfo = ZoneInfo(report_station.tz_name)
    report_lcl = utc_to_local(report_utc, report_tzinfo, s_dutyperiod.report_time.lcl)

    e_dutyperiod = ET.DutyPeriod(
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
    return (e_dutyperiod, state)
