"""FILE: translate_trips.py."""

import logging
from datetime import date, timedelta
from zoneinfo import ZoneInfo

from pbs_parse.common.get_airport_info import get_airport_info_from_iata
from pbs_parse.common.parse_duration import parse_duration
from pbs_parse.pbs_2022_01.expand_from_parsed.state import State
from pbs_parse.pbs_2022_01.expand_from_parsed.translate_dutyperiods import (
    translate_dutyperiods,
)
from pbs_parse.pbs_2022_01.models.collated_trip import CollatedTrip
from pbs_parse.pbs_2022_01.models.expanded import (
    BaseEquipment,
    ExpandedTrip,
    ExpandedTripSource,
    Operation,
    Position,
)

logger = logging.getLogger(__name__)
UTC = ZoneInfo("UTC")


def translate_trips(collated_trip: CollatedTrip, state: State) -> list[ExpandedTrip]:
    """translate_trips.

    Args:
        collated_trip (CollatedTrip): _description_
        state (State): _description_

    Returns:
        list[ExpandedTrip]: _description_
    """
    trips: list[ExpandedTrip] = []
    for start_date in state.start_dates:
        state.reset()
        trip = translate_trip(
            collated_trip=collated_trip, start_date=start_date, state=state
        )
        trips.append(trip)
    return trips


def translate_trip(
    collated_trip: CollatedTrip, start_date: date, state: State
) -> ExpandedTrip:
    """translate_trip.

    Args:
        collated_trip (CollatedTrip): _description_
        start_date (date): _description_
        state (State): _description_

    Returns:
        ExpandedTrip: _description_
    """
    dutyperiods = translate_dutyperiods(
        start_date=start_date,
        collated_dutyperiods=collated_trip.dutyperiods,
        state=state,
    )
    positions = [Position(name=x) for x in collated_trip.trip_header.data["positions"]]
    operations = [
        Operation(name=x) for x in collated_trip.trip_header.data["operations"]
    ]
    flight_time = timedelta(
        seconds=sum([x.flight_time.total_seconds() for x in dutyperiods])
    )
    operating_time = parse_duration(collated_trip.trip_footer.data["block"])
    soft_time = parse_duration(collated_trip.trip_footer.data["synth"])
    tafb = parse_duration(collated_trip.trip_footer.data["tafb"])
    try:
        satellite_base = get_airport_info_from_iata(
            iata=collated_trip.page_footer.data["satellite_base"]
        )
    except ValueError:
        satellite_base = None
    base_equipment = BaseEquipment(
        base=state.base,
        satellite_base=satellite_base,
        equipment=collated_trip.page_footer.data["equipment"],
    )
    source = ExpandedTripSource(
        txt_file=state.parsed_source.txt_file,
        page_lines=state.parsed_source.page_lines,
        trip_lines=state.parsed_source.trip_lines,
        parsed_trip=state.source_file,
    )
    expanded_trip = ExpandedTrip(
        source=source,
        trip_number=collated_trip.trip_header.data["trip_number"],
        base_equipment=base_equipment,
        positions=positions,
        operations=operations,
        special_qual=collated_trip.trip_header.data["special_qual"],
        start_station=dutyperiods[0].report_station,
        start_utc=dutyperiods[0].report_utc,
        start_lcl=dutyperiods[0].report_lcl,
        start_hbt=dutyperiods[0].report_hbt,
        end_station=dutyperiods[-1].release_station,
        end_utc=dutyperiods[-1].release_utc,
        end_lcl=dutyperiods[-1].release_lcl,
        end_hbt=dutyperiods[-1].release_hbt,
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        tafb=tafb,
        dutyperiods=dutyperiods,
    )
    return expanded_trip
