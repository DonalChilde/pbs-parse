"""FILE: translate_flights.py."""

import logging
from collections.abc import Sequence

from pfmsoft.state_parser.model import ParsedIndexedString
from whenever import TimeDelta, ZonedDateTime

from pbs_parse.common.get_airport_info import get_airport_info_from_iata
from pbs_parse.common.parse_duration_whenever import parse_duration
from pbs_parse.pbs_2022_01.expand_from_parsed.state import State
from pbs_parse.pbs_2022_01.models.expanded import AirportInfo, Flight

ZERO_DELTA = TimeDelta(seconds=0)
logger = logging.getLogger(__name__)


def translate_flights(
    first_departure: ZonedDateTime,
    parsed_flights: Sequence[ParsedIndexedString],
    state: State,
) -> list[Flight]:
    """translate_flights.

    Args:
        first_departure (ZonedDateTime): _description_
        parsed_flights (Sequence[ParsedIndexedString]): _description_
        state (State): _description_

    Returns:
        list[Flight]: _description_
    """
    flights: list[Flight] = []
    departure = first_departure
    for idx, parsed_flight in enumerate(parsed_flights, start=1):
        state.flight_idx = idx
        logger.debug(
            "Translating flight %d with departure %s",
            state.flight_idx,
            departure,
        )
        departure_station = get_airport_info_from_iata(
            parsed_flight.data["departure_station"]
        )
        expanded_flight = translate_flight(
            departure=departure,
            departure_station=departure_station,
            parsed_flight=parsed_flight,
            state=state,
        )
        departure = expanded_flight.arrival + expanded_flight.ground_time
        flights.append(expanded_flight)
    return flights


def translate_flight(
    departure: ZonedDateTime,
    departure_station: AirportInfo,
    parsed_flight: ParsedIndexedString,
    state: State,
) -> Flight:
    """translate_flight.

    Args:
        departure (ZonedDateTime): _description_
        departure_station (AirportInfo): _description_
        parsed_flight (ParsedIndexedString): _description_
        state (State): _description_

    Raises:
        ValueError: _description_

    Returns:
        Flight: _description_
    """
    if departure.tz != departure_station.tz_name:
        departure = departure.to_tz(departure_station.tz_name)
    arrival_station = get_airport_info_from_iata(
        iata=parsed_flight.data["arrival_station"]
    )
    operating_time = parse_duration(parsed_flight.data["block"])
    soft_time = parse_duration(parsed_flight.data["synth"])
    if operating_time > ZERO_DELTA and soft_time == ZERO_DELTA:
        arrival = (departure + operating_time).to_tz(arrival_station.tz_name)
    elif operating_time == ZERO_DELTA and soft_time > ZERO_DELTA:
        arrival = (departure + soft_time).to_tz(arrival_station.tz_name)
    else:
        raise ValueError(
            f"Inconsistent soft and operating times for parsed flight. {state.source_file}: {parsed_flight}"
        )
    flight_time = arrival - departure
    try:
        ground_time = parse_duration(parsed_flight.data["ground"])
    except ValueError:
        ground_time = ZERO_DELTA
    expanded_flight = Flight(
        eq_code=parsed_flight.data["equipment_code"],
        number=parsed_flight.data["flight_number"],
        departure_station=departure_station,
        departure=departure,
        arrival_station=arrival_station,
        arrival=arrival,
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
