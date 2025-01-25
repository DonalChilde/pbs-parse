"""FILE: translate_layover.py."""

from datetime import datetime
from zoneinfo import ZoneInfo

from pfmsoft.state_parser.model import ParsedIndexedString

from pbs_parse.common.get_airport_info import get_airport_info_from_iata
from pbs_parse.common.parse_duration import parse_duration
from pbs_parse.pbs_2022_01.expand_from_parsed.next_utc import next_utc
from pbs_parse.pbs_2022_01.expand_from_parsed.state import State
from pbs_parse.pbs_2022_01.models.expanded import Hotel, Layover, Transportation


def translate_layover(
    dutyperiod_release_utc: datetime,
    layover: ParsedIndexedString | None,
    hotel_info: list[ParsedIndexedString],
    state: State,
) -> Layover | None:
    """translate_layover.

    Args:
        dutyperiod_release_utc (datetime): _description_
        layover (ParsedIndexedString | None): _description_
        hotel_info (list[ParsedIndexedString]): _description_
        state (State): _description_

    Returns:
        Layover | None: _description_
    """
    if layover is None:
        return None
    layover_station = get_airport_info_from_iata(iata=layover.data["layover_city"])

    rest = parse_duration(layover.data["rest"])
    end_utc = next_utc(utc_datetime=dutyperiod_release_utc, delta=rest)
    hotel = Hotel(
        name=layover.data["hotel_name"],
        phone=layover.data["hotel_phone"],
        transportation=[],
    )
    expanded_layover = Layover(
        layover_station=layover_station,
        start_utc=dutyperiod_release_utc,
        start_lcl=dutyperiod_release_utc.astimezone(ZoneInfo(layover_station.tz_name)),
        start_hbt=dutyperiod_release_utc.astimezone(state.hbt_tzinfo),
        end_utc=end_utc,
        end_lcl=end_utc.astimezone(ZoneInfo(layover_station.tz_name)),
        end_hbt=end_utc.astimezone(state.hbt_tzinfo),
        rest=rest,
        hotels=[hotel],
    )
    expanded_layover.hotels = translate_hotels(
        hotels=expanded_layover.hotels, parsed_lines=hotel_info
    )
    return expanded_layover


def translate_hotels(
    hotels: list[Hotel], parsed_lines: list[ParsedIndexedString]
) -> list[Hotel]:
    """translate_hotels.

    Args:
        hotels (list[Hotel]): _description_
        parsed_lines (list[ParsedIndexedString]): _description_

    Raises:
        ValueError: _description_

    Returns:
        list[Hotel]: _description_
    """
    for line in parsed_lines:
        match line.id:
            case "transportation":
                transportation = Transportation(
                    name=line.data["name"], phone=line.data["phone"]
                )
                hotels[0].transportation.append(transportation)
            case "hotel_additional":
                hotel = Hotel(
                    name=line.data["name"], phone=line.data["phone"], transportation=[]
                )
                hotels.append(hotel)
            case "transportation_additional":
                transportation = Transportation(
                    name=line.data["name"], phone=line.data["phone"]
                )
                hotels[0].transportation.append(transportation)
            case _:
                raise ValueError(
                    f"Got an unhandled line id while translating hotel info. {line}"
                )
    return hotels
