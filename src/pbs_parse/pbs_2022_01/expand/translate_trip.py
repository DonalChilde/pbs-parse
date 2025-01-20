"""FILE: translate_trip.py."""

import logging
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pbs_parse.pbs_2022_01.models.expanded as ET
import pbs_parse.pbs_2022_01.models.structured as ST
from pbs_parse.pbs_2022_01.expand.state import State
from pbs_parse.pbs_2022_01.expand.translate_dutyperiods import translate_dutyperiods

logger = logging.getLogger(__name__)
UTC = ZoneInfo("UTC")


def translate_trip(
    s_trip: ST.StructuredTrip, start_date: date, source_file: str, state: State
) -> tuple[ET.ExpandedTrip, State]:
    """Translate a StructuredTrip that starts on a particular date."""
    logger.info(
        "Translating trip %s - %s with start date %s uuid: %s",
        s_trip.number,
        s_trip.page_footer.base,
        start_date.isoformat(),
        s_trip.uuid,
    )
    # base_airport = model.get_airport_code_from_iata(s_trip.page_footer.base)
    first_report = time.fromisoformat(s_trip.dutyperiods[0].report_time.lcl)
    # Should be unambiguous unless start time is in the fold, Nov. dst switch 2am sunday.
    report_utc = datetime.combine(
        start_date, first_report, state.hbt_tzinfo
    ).astimezone(UTC)
    dutyperiods, state = translate_dutyperiods(
        first_report_utc=report_utc, s_dutyperiods=s_trip.dutyperiods, state=state
    )
    positions = [ET.Position(name=x) for x in s_trip.positions]
    operations = [ET.Operation(name=x) for x in s_trip.operations]
    flight_time = timedelta(
        seconds=sum([x.flight_time.total_seconds() for x in dutyperiods])
    )
    operating_time = ST.parse_duration(s_trip.block)
    soft_time = ST.parse_duration(s_trip.synth)
    tafb = ST.parse_duration(s_trip.tafb)
    try:
        satellite_base = ET.get_airport_code_from_iata(
            iata=s_trip.page_footer.satellite_base
        )
    except ValueError:
        satellite_base = None
    base_equipment = ET.BaseEquipment(
        base=state.base,
        satellite_base=satellite_base,
        equipment=s_trip.page_footer.equipment,
    )
    source = ET.ExpandedTripSource(
        txt_file=s_trip.source.txt_file,
        page_lines=s_trip.source.page_lines,
        trip_lines=s_trip.source.trip_lines,
        parsed_trip=s_trip.source.parsed_trip,
        structured_trip=source_file,
    )
    e_trip = ET.ExpandedTrip(
        source=source,
        source_uuid=s_trip.uuid,
        source_idx=s_trip.idx,
        trip_number=s_trip.number,
        base_equipment=base_equipment,
        positions=positions,
        operations=operations,
        special_qual=s_trip.special_qual,
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
    return (e_trip, state)
