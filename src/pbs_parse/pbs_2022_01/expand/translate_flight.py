"""FILE: translate_flight.py."""

import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pbs_parse.pbs_2022_01.models.expanded as ET
import pbs_parse.pbs_2022_01.models.structured as ST
from pbs_parse.pbs_2022_01.expand.delta_dt import delta_dt
from pbs_parse.pbs_2022_01.expand.state import State

logger = logging.getLogger(__name__)


def translate_flight(
    departure_utc: datetime,
    departure_station: ET.AirportCode,
    s_flight: ST.Flight,
    state: State,
) -> tuple[ET.Flight, State]:
    """translate_flight.

    Args:
        departure_utc (datetime): _description_
        departure_station (ET.AirportCode): _description_
        s_flight (ST.Flight): _description_
        state (State): _description_

    Raises:
        ValueError: _description_

    Returns:
        tuple[ET.Flight, State]: _description_
    """
    zero = timedelta(seconds=0)
    arrival_station = ET.get_airport_code_from_iata(iata=s_flight.arrival_station)
    operating_time = ST.parse_duration(s_flight.block)
    soft_time = ST.parse_duration(s_flight.synth)
    if operating_time > zero and soft_time == zero:
        arrival_utc, state = delta_dt(
            utc_ref=departure_utc,
            td=operating_time,
            lcl_ref=s_flight.arrival_time.lcl,
            lcl_tz=arrival_station.tz_name,
            field_name="arrival operating time",
            state=state,
        )
    elif operating_time == zero and soft_time > zero:
        arrival_utc, state = delta_dt(
            utc_ref=departure_utc,
            td=soft_time,
            lcl_ref=s_flight.arrival_time.lcl,
            lcl_tz=arrival_station.tz_name,
            field_name="arrival soft time",
            state=state,
        )
    else:
        raise ValueError(
            f"Inconsistent soft and operating times for structured flight. {s_flight}"
        )
    flight_time = arrival_utc - departure_utc

    try:
        ground_time = ST.parse_duration(s_flight.ground)
    except ValueError:
        ground_time = timedelta(hours=0)

    e_flight = ET.Flight(
        eq_code=s_flight.equipment_code,
        number=s_flight.flight_number,
        departure_station=departure_station,
        departure_utc=departure_utc,
        departure_lcl=departure_utc.astimezone(ZoneInfo(departure_station.tz_name)),
        departure_hbt=departure_utc.astimezone(state.hbt_tzinfo),
        arrival_station=arrival_station,
        arrival_utc=arrival_utc,
        arrival_lcl=arrival_utc.astimezone(ZoneInfo(arrival_station.tz_name)),
        arrival_hbt=arrival_utc.astimezone(state.hbt_tzinfo),
        deadhead=bool(s_flight.deadhead),
        deadhead_code=s_flight.deadhead_code,
        crewmeal=s_flight.crew_meal,
        eq_change=bool(s_flight.equipment_change),
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        ground_time=ground_time,
    )
    return (e_flight, state)
