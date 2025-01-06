"""FILE: translate_flights.py."""

import logging
from collections.abc import Sequence
from datetime import datetime

import pbs_parse.pbs_2022_01.models.expanded as ET
import pbs_parse.pbs_2022_01.models.structured as ST
from pbs_parse.pbs_2022_01.expand.state import State
from pbs_parse.pbs_2022_01.expand.translate_flight import translate_flight

logger = logging.getLogger(__name__)


def translate_flights(
    first_departure_utc: datetime, s_flights: Sequence[ST.Flight], state: State
) -> tuple[list[ET.Flight], State]:
    """translate_flights.

    Args:
        first_departure_utc (datetime): _description_
        s_flights (Sequence[ST.Flight]): _description_
        state (State): _description_

    Returns:
        tuple[list[ET.Flight], State]: _description_
    """
    flights: list[ET.Flight] = []
    departure_utc = first_departure_utc
    for idx, s_flight in enumerate(s_flights):
        state.flight_idx = idx + 1
        logger.debug(
            "Translating flight %d with departure_utc %s",
            state.flight_idx,
            departure_utc.isoformat(),
        )
        departure_station = ET.get_airport_code_from_iata(s_flight.departure_station)
        e_flight, state = translate_flight(
            departure_utc=departure_utc,
            departure_station=departure_station,
            s_flight=s_flight,
            state=state,
        )
        departure_utc = e_flight.arrival_utc + e_flight.ground_time
        flights.append(e_flight)
    return (flights, state)
