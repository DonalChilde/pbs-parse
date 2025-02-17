"""FILE: collate_parsed.py."""

import logging
from typing import Any

from pbs_parse.pbs_2022_01.models.collated_trip import CollatedDutyPeriod, CollatedTrip
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.snippets.indexed_string_state_parser.model import ParsedIndexedString

logger = logging.getLogger(__name__)


def collate_parsed(parsed_trip: ParsedTrip) -> CollatedTrip:
    """collate_parsed.

    Args:
        parsed_trip (ParsedTrip): _description_

    Returns:
        Trip: _description_
    """
    trip_line_dict: dict[str, Any] = {}
    dp_list: list[dict[str, Any]] = []
    trip_line_dict["duty_periods"] = dp_list
    for parsed_line in parsed_trip.parsed_lines:
        match parsed_line.id:
            case "page_header_1":
                trip_line_dict["page_header_1"] = parsed_line
            case "page_header_2":
                trip_line_dict["page_header_2"] = parsed_line
            case "trip_header":
                trip_line_dict["trip_header"] = parsed_line
            case "duty_period_report":
                flights: list[ParsedIndexedString] = []
                trip_line_dict["duty_periods"].append(
                    {
                        "report": parsed_line,
                        "flights": flights,
                        "layover": None,
                        "hotel": [],
                    }
                )
            case "flight":
                trip_line_dict["duty_periods"][-1]["flights"].append(parsed_line)
            case "duty_period_release":
                trip_line_dict["duty_periods"][-1]["release"] = parsed_line
            case "layover":
                trip_line_dict["duty_periods"][-1]["layover"] = parsed_line
            case "transportation":
                trip_line_dict["duty_periods"][-1]["hotel"].append(parsed_line)  # type: ignore
            case "hotel_additional":
                trip_line_dict["duty_periods"][-1]["hotel"].append(parsed_line)  # type: ignore
            case "transportation_additional":
                trip_line_dict["duty_periods"][-1]["hotel"].append(parsed_line)  # type: ignore
            case "trip_footer":
                trip_line_dict["trip_footer"] = parsed_line
            case "page_footer":
                trip_line_dict["page_footer"] = parsed_line
            case _:
                logger.info(f"trip line organizer skipped this id: {parsed_line.id}")
                pass

    return dict_to_trip(trip_line_dict)


def dict_to_trip(data: dict[str, Any]) -> CollatedTrip:
    """dict_to_trip.

    Args:
        data (dict[str, Any]): _description_

    Returns:
        Trip: _description_
    """
    dutyperiods: list[CollatedDutyPeriod] = []
    for dp in data["duty_periods"]:
        if dp["layover"] is None:
            layover = None
        else:
            layover = dp["layover"]
        dutyperiods.append(
            CollatedDutyPeriod(
                report=dp["report"],
                flights=dp["flights"],
                release=dp["release"],
                layover=layover,
                hotel=dp["hotel"],
            )
        )
    trip = CollatedTrip(
        page_header_1=data["page_header_1"],
        page_header_2=data["page_header_2"],
        trip_header=data["trip_header"],
        trip_footer=data["trip_footer"],
        page_footer=data["page_footer"],
        dutyperiods=dutyperiods,
    )
    return trip
