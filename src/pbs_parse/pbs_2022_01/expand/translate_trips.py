"""FILE: translate_trips.py."""

from datetime import date

import pbs_parse.pbs_2022_01.models.expanded as ET
import pbs_parse.pbs_2022_01.models.structured as ST
from pbs_parse.pbs_2022_01.expand.state import State
from pbs_parse.pbs_2022_01.expand.translate_trip import translate_trip


def translate_trips(
    s_trip: ST.StructuredTrip, state: State
) -> tuple[list[ET.ExpandedTrip], State]:
    """translate_trips.

    Args:
        s_trip (ST.StructuredTrip): _description_
        state (State): _description_

    Returns:
        tuple[list[ET.ExpandedTrip], State]: _description_
    """
    start_dates = ST.build_start_dates(
        effective_from=date.fromisoformat(s_trip.external.effective_from),
        effective_to=date.fromisoformat(s_trip.external.effective_to),
        calendar=s_trip.calendar,
    )
    trips: list[ET.ExpandedTrip] = []
    for start_date in start_dates:
        trip, state = translate_trip(s_trip=s_trip, start_date=start_date, state=state)
        trips.append(trip)
    return (trips, state)
