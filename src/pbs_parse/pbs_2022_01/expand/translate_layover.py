"""FILE: translate_layover.py."""

import logging
from collections.abc import Sequence
from datetime import datetime
from zoneinfo import ZoneInfo

import pbs_parse.pbs_2022_01.models.expanded as ET
import pbs_parse.pbs_2022_01.models.structured as ST
from pbs_parse.pbs_2022_01.expand.delta_dt import delta_dt
from pbs_parse.pbs_2022_01.expand.state import State

logger = logging.getLogger(__name__)


def translate_layover(
    dutyperiod_release_utc: datetime,
    next_report_lcl: str,
    s_layover: ST.Layover | None,
    state: State,
) -> tuple[ET.Layover | None, State]:
    """translate_layover.

    Args:
        dutyperiod_release_utc (datetime): _description_
        next_report_lcl (str): _description_
        s_layover (ST.Layover | None): _description_
        state (State): _description_

    Returns:
        tuple[ET.Layover | None, State]: _description_
    """
    if s_layover is None:
        logger.debug("No Layover.")
        return (None, state)
    logger.debug(
        "Translating layover with start %s", dutyperiod_release_utc.isoformat()
    )
    hotels, state = translate_hotels(s_hotels=s_layover.hotels, state=state)
    layover_station = ET.get_airport_code_from_iata(iata=s_layover.city)

    rest = ST.parse_duration(s_layover.rest)
    end_utc, state = delta_dt(
        utc_ref=dutyperiod_release_utc,
        td=rest,
        lcl_ref=next_report_lcl,
        lcl_tz=layover_station.tz_name,
        field_name="Layover end",
        state=state,
    )
    e_layover = ET.Layover(
        layover_station=layover_station,
        start_utc=dutyperiod_release_utc,
        start_lcl=dutyperiod_release_utc.astimezone(ZoneInfo(layover_station.tz_name)),
        start_hbt=dutyperiod_release_utc.astimezone(state.hbt_tzinfo),
        end_utc=end_utc,
        end_lcl=end_utc.astimezone(ZoneInfo(layover_station.tz_name)),
        end_hbt=end_utc.astimezone(state.hbt_tzinfo),
        rest=rest,
        hotels=hotels,
    )
    return (e_layover, state)


def translate_hotels(
    s_hotels: Sequence[ST.Hotel], state: State
) -> tuple[list[ET.Hotel], State]:
    """translate_hotels.

    Args:
        s_hotels (Sequence[ST.Hotel]): _description_
        state (State): _description_

    Returns:
        tuple[list[ET.Hotel], State]: _description_
    """
    hotels: list[ET.Hotel] = []
    for idx, s_hotel in enumerate(s_hotels, start=1):
        logger.debug("Translating hotel %d", idx)
        e_hotel, state = translate_hotel(s_hotel=s_hotel, state=state)
        hotels.append(e_hotel)
    return (hotels, state)


def translate_hotel(s_hotel: ST.Hotel, state: State) -> tuple[ET.Hotel, State]:
    """translate_hotel.

    Args:
        s_hotel (ST.Hotel): _description_
        state (State): _description_

    Returns:
        tuple[ET.Hotel, State]: _description_
    """
    transportation: list[ET.Transportation] = []
    for idx, s_trans in enumerate(s_hotel.transportation, start=1):
        logger.debug("Translating transportation %d", idx)
        trans = ET.Transportation(name=s_trans.name, phone=s_trans.phone)
        transportation.append(trans)
    hotel = ET.Hotel(
        name=s_hotel.name, phone=s_hotel.phone, transportation=transportation
    )
    return (hotel, state)
