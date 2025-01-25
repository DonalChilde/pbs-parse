"""FILE: translate_flights.py."""

import logging
from collections.abc import Sequence
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from pfmsoft.state_parser.model import ParsedIndexedString

from pbs_parse.common.get_airport_info import get_airport_info_from_iata
from pbs_parse.common.parse_duration import parse_duration
from pbs_parse.pbs_2022_01.expand_from_parsed.next_utc import next_utc
from pbs_parse.pbs_2022_01.expand_from_parsed.state import State
from pbs_parse.pbs_2022_01.models.expanded import AirportInfo, Flight

ZERO_DELTA = timedelta(seconds=0)
logger = logging.getLogger(__name__)


def translate_flights(
    first_departure_utc: datetime,
    parsed_flights: Sequence[ParsedIndexedString],
    state: State,
) -> list[Flight]:
    """translate_flights.

    Args:
        first_departure_utc (datetime): _description_
        parsed_flights (Sequence[ParsedIndexedString]): _description_
        state (State): _description_

    Returns:
        list[Flight]: _description_
    """
    flights: list[Flight] = []
    departure_utc = first_departure_utc
    for idx, parsed_flight in enumerate(parsed_flights, start=1):
        state.flight_idx = idx
        logger.debug(
            "Translating flight %d with departure_utc %s",
            state.flight_idx,
            departure_utc,
        )
        departure_station = get_airport_info_from_iata(
            parsed_flight.data["departure_station"]
        )
        expanded_flight = translate_flight(
            departure_utc=departure_utc,
            departure_station=departure_station,
            parsed_flight=parsed_flight,
            state=state,
        )
        departure_utc = expanded_flight.arrival_utc + expanded_flight.ground_time
        flights.append(expanded_flight)
    return flights


def translate_flight(
    departure_utc: datetime,
    departure_station: AirportInfo,
    parsed_flight: ParsedIndexedString,
    state: State,
) -> Flight:
    """translate_flight.

    Args:
        departure_utc (datetime): _description_
        departure_station (AirportInfo): _description_
        parsed_flight (ParsedIndexedString): _description_
        state (State): _description_

    Raises:
        ValueError: _description_

    Returns:
        Flight: _description_
    """
    arrival_station = get_airport_info_from_iata(
        iata=parsed_flight.data["arrival_station"]
    )
    operating_time = parse_duration(parsed_flight.data["block"])
    soft_time = parse_duration(parsed_flight.data["synth"])
    if operating_time > ZERO_DELTA and soft_time == ZERO_DELTA:
        arrival_utc = next_utc(utc_datetime=departure_utc, delta=operating_time)
    elif operating_time == ZERO_DELTA and soft_time > ZERO_DELTA:
        arrival_utc = next_utc(utc_datetime=departure_utc, delta=soft_time)
    else:
        raise ValueError(
            f"Inconsistent soft and operating times for parsed flight. {state.source_file}: {parsed_flight}"
        )
    flight_time = arrival_utc - departure_utc
    try:
        ground_time = parse_duration(parsed_flight.data["ground"])
    except ValueError:
        ground_time = ZERO_DELTA
    expanded_flight = Flight(
        eq_code=parsed_flight.data["equipment_code"],
        number=parsed_flight.data["flight_number"],
        departure_station=departure_station,
        departure_utc=departure_utc,
        departure_lcl=departure_utc.astimezone(ZoneInfo(departure_station.tz_name)),
        departure_hbt=departure_utc.astimezone(state.hbt_tzinfo),
        arrival_station=arrival_station,
        arrival_utc=arrival_utc,
        arrival_lcl=arrival_utc.astimezone(ZoneInfo(arrival_station.tz_name)),
        arrival_hbt=arrival_utc.astimezone(state.hbt_tzinfo),
        deadhead=bool(parsed_flight.data["deadhead"]),
        deadhead_code=parsed_flight.data["deadhead_code"],
        crewmeal=parsed_flight.data["crew_meal"],
        eq_change=bool(parsed_flight.data["equipment_change"]),
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        ground_time=ground_time,
    )
    return expanded_flight
