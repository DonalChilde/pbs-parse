"""FILE: translate_trips.py."""

import pbs_parse.pbs_2022_01.models.expanded as ET
import pbs_parse.pbs_2022_01.models.structured as ST
from pbs_parse.pbs_2022_01.expand.state import State
from pbs_parse.pbs_2022_01.expand.translate_trip import translate_trip


def translate_trips(
    s_trip: ST.StructuredTrip, source_file: str, state: State
) -> tuple[list[ET.ExpandedTrip], State]:
    """translate_trips.

    Args:
        s_trip (ST.StructuredTrip): _description_
        source_file (str): _description_
        state (State): _description_

    Returns:
        tuple[list[ET.ExpandedTrip], State]: _description_
    """
    start_dates = ST.build_start_dates(
        effective_from=s_trip.external.effective_from,
        effective_to=s_trip.external.effective_to,
        calendar=s_trip.calendar,
    )
    trips: list[ET.ExpandedTrip] = []
    for start_date in start_dates:
        trip, state = translate_trip(
            s_trip=s_trip, source_file=source_file, start_date=start_date, state=state
        )
        trips.append(trip)
    return (trips, state)
