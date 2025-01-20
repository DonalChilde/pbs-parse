"""Translate a parsed to structured trip."""

import logging
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from pfmsoft.state_parser.model import ParsedIndexedString

from pbs_parse.pbs_2022_01.models import grammar_TD as linesTD
from pbs_parse.pbs_2022_01.models import structured
from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER, ParsedTrip

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class LayoverLines:
    """Temporary gathering of data."""

    layover: ParsedIndexedString
    lines: list[ParsedIndexedString] = field(default_factory=list)
    """Transportation and additional hotels."""


@dataclass(slots=True)
class DutyPeriodLines:
    """Temporary gathering of data."""

    report: ParsedIndexedString
    flights: list[ParsedIndexedString]
    release: ParsedIndexedString
    layover: LayoverLines | None


@dataclass(slots=True)
class TripLines:
    """Temporary gathering of data."""

    page_header_2: ParsedIndexedString
    trip_header: ParsedIndexedString
    trip_footer: ParsedIndexedString
    page_footer: ParsedIndexedString
    duty_periods: list[DutyPeriodLines] = field(default_factory=list)


def structure_trip_from_file(
    path_in: Path, effective_from: date, effective_to: date
) -> structured.StructuredTrip:
    """Load a ParsedTrip from file and translate it."""
    parsed_trip = PARSED_TRIP_SERIALIZER.load_from_json(path_in=path_in)
    return structure_trip(parsed_trip=parsed_trip, source_file=path_in.name)


# def structure_trips(
#     parsed_trips: Iterable[ParsedTrip],
#     effective_from: date,
#     effective_to: date,
#     observer: Callable[[structured.StructuredTrip], None] | None = None,
# ) -> Iterator[structured.StructuredTrip]:
#     """Structure parsed trips, with optional observer.

#     All trips are expected to have the same effective from-to dates.

#     Args:
#         parsed_trips (Iterable[ParsedTrip]): _description_
#         effective_from (date): _description_
#         effective_to (date): _description_
#         observer (Callable[[structured.StructuredTrip], None] | None, optional): _description_. Defaults to None.

#     Yields:
#         Iterator[structured.StructuredTrip]: _description_
#     """
#     for parsed in parsed_trips:
#         structured = structure_trip(
#             parsed_trip=parsed, effective_from=effective_from, effective_to=effective_to
#         )
#         if observer:
#             observer(structured)
#         yield structured


def structure_trip(
    parsed_trip: ParsedTrip, source_file: str
) -> structured.StructuredTrip:
    """Translate a ParsedTrip."""
    trip = _translate_trip(
        source_file=source_file,
        parsed_trip=parsed_trip,
    )
    return trip


def _translate_flight(parsed_data: linesTD.Flight, idx: int) -> structured.Flight:
    flight = structured.Flight(
        idx=str(idx),
        dutyperiod_idx=parsed_data["dutyperiod_idx"],
        depart_day=parsed_data["depart_day"],
        arrive_day=parsed_data["arrive_day"],
        equipment_code=parsed_data["equipment_code"],
        flight_number=parsed_data["flight_number"],
        deadhead=parsed_data["deadhead"],
        deadhead_code=parsed_data["deadhead_code"],
        departure_station=parsed_data["departure_station"],
        departure_time=structured.DualTime(**parsed_data["departure_time"]),
        crew_meal=parsed_data["crew_meal"],
        arrival_station=parsed_data["arrival_station"],
        arrival_time=structured.DualTime(**parsed_data["arrival_time"]),
        block=parsed_data["block"],
        synth=parsed_data["synth"],
        ground=parsed_data["ground"],
        equipment_change=parsed_data["equipment_change"],
    )
    return flight


def _translate_dutyperiod(
    dutyperiod_lines: DutyPeriodLines, idx: int
) -> structured.DutyPeriod:
    flights = [
        _translate_flight(x.data, idx)  # type: ignore
        for idx, x in enumerate(dutyperiod_lines.flights, start=1)
    ]
    if dutyperiod_lines.layover is None:
        layover = None
    else:
        layover = _translate_layover(dutyperiod_lines.layover)
    dutyperiod = structured.DutyPeriod(
        idx=str(idx),
        report_time=structured.DualTime(**dutyperiod_lines.report.data["report"]),
        release_time=structured.DualTime(**dutyperiod_lines.release.data["release"]),
        block=dutyperiod_lines.release.data["block"],
        synth=dutyperiod_lines.release.data["synth"],
        total_pay=dutyperiod_lines.release.data["total_pay"],
        duty=dutyperiod_lines.release.data["duty"],
        flight_duty=dutyperiod_lines.release.data["flight_duty"],
        layover=layover,
        flights=flights,
    )
    return dutyperiod


def _translate_layover(layover_lines: LayoverLines) -> structured.Layover:
    layover = structured.Layover(
        rest=layover_lines.layover.data["rest"],
        city=layover_lines.layover.data["layover_city"],
        hotels=_translate_hotels(
            layover_lines.lines,
            name=layover_lines.layover.data["hotel_name"],
            phone=layover_lines.layover.data["hotel_phone"],
        ),
    )
    return layover


def _translate_hotels(
    lines: list[ParsedIndexedString], name: str, phone: str
) -> list[structured.Hotel]:
    first_hotel = structured.Hotel(name=name, phone=phone)
    hotels: list[structured.Hotel] = [first_hotel]
    for line in lines:
        if line.id == "transportation":
            hotels[-1].transportation.append(
                structured.Transportation(
                    name=line.data["name"], phone=line.data["phone"]
                )
            )
        elif line.id == "transportation_additional":
            hotels[-1].transportation.append(
                structured.Transportation(
                    name=line.data["name"], phone=line.data["phone"]
                )
            )
        elif line.id == "hotel_additional":
            hotels.append(
                structured.Hotel(name=line.data["name"], phone=line.data["phone"])
            )

    return hotels


def _translate_trip(
    parsed_trip: ParsedTrip,
    source_file: str,
    # effective_from: date,
    # effective_to: date,
    # source_uuid: str,
) -> structured.StructuredTrip:
    trip_lines = _organize_lines(parsed_trip=parsed_trip)
    calendar = _collect_calendar(parsed_trip=parsed_trip)
    dutyperiods: list[structured.DutyPeriod] = [
        _translate_dutyperiod(x, idx)
        for idx, x in enumerate(trip_lines.duty_periods, start=1)
    ]
    # external = structured.ExternalData(
    #     effective_from=effective_from.isoformat(),
    #     effective_to=effective_to.isoformat(),
    # )
    external = deepcopy(parsed_trip.external)
    page_header = structured.PageHeader(
        from_date=structured.MonthDay(**trip_lines.page_header_2.data["from_date"]),
        to_date=structured.MonthDay(**trip_lines.page_header_2.data["to_date"]),
    )
    page_footer = structured.PageFooter(
        issued=trip_lines.page_footer.data["issued"],
        effective=trip_lines.page_footer.data["effective"],
        base=trip_lines.page_footer.data["base"],
        satellite_base=trip_lines.page_footer.data["satellite_base"],
        equipment=trip_lines.page_footer.data["equipment"],
        division=trip_lines.page_footer.data["division"],
        page=trip_lines.page_footer.data["page"],
    )
    source = structured.StructuredTripSource(
        txt_file=parsed_trip.source.txt_file,
        page_lines=parsed_trip.source.page_lines,
        trip_lines=parsed_trip.source.trip_lines,
        parsed_trip=source_file,
    )
    trip = structured.StructuredTrip(
        source=source,
        source_uuid=parsed_trip.uuid,
        idx=parsed_trip.idx,
        number=trip_lines.trip_header.data["trip_number"],
        ops_count=trip_lines.trip_header.data["ops_count"],
        positions=trip_lines.trip_header.data["positions"],
        operations=trip_lines.trip_header.data["operations"],
        special_qual=trip_lines.trip_header.data["special_qual"],
        block=trip_lines.trip_footer.data["block"],
        synth=trip_lines.trip_footer.data["synth"],
        total_pay=trip_lines.trip_footer.data["total_pay"],
        tafb=trip_lines.trip_footer.data["tafb"],
        calendar=calendar,
        external=external,
        page_header=page_header,
        page_footer=page_footer,
        dutyperiods=dutyperiods,
    )
    return trip


def _collect_calendar(parsed_trip: ParsedTrip) -> list[str]:
    calendar: list[str] = []
    for parsed_line in parsed_trip.parsed_lines:
        maybe = parsed_line.data.get("calendar_entries", [])
        if maybe:
            calendar.extend(maybe)
    return calendar


def _organize_lines(parsed_trip: ParsedTrip) -> TripLines:
    trip_line_dict: dict[str, Any] = {}
    dp_list: list[dict[str, Any]] = []
    trip_line_dict["duty_periods"] = dp_list
    for parsed_line in parsed_trip.parsed_lines:
        match parsed_line.id:
            case "page_header_2":
                trip_line_dict["page_header_2"] = parsed_line
            case "trip_header":
                trip_line_dict["trip_header"] = parsed_line
            case "duty_period_report":
                flights: list[ParsedIndexedString] = []
                trip_line_dict["duty_periods"].append(
                    {"report": parsed_line, "flights": flights, "layover": None}
                )
            case "flight":
                trip_line_dict["duty_periods"][-1]["flights"].append(parsed_line)
            case "duty_period_release":
                trip_line_dict["duty_periods"][-1]["release"] = parsed_line
            case "layover":
                trip_line_dict["duty_periods"][-1]["layover"] = {
                    "layover": parsed_line,
                    "lines": [],
                }
            case "transportation":
                trip_line_dict["duty_periods"][-1]["layover"]["lines"].append(  # type: ignore
                    parsed_line
                )
            case "hotel_additional":
                trip_line_dict["duty_periods"][-1]["layover"]["lines"].append(  # type: ignore
                    parsed_line
                )
            case "transportation_additional":
                trip_line_dict["duty_periods"][-1]["layover"]["lines"].append(  # type: ignore
                    parsed_line
                )
            case "trip_footer":
                trip_line_dict["trip_footer"] = parsed_line
            case "page_footer":
                trip_line_dict["page_footer"] = parsed_line
            case _:
                logger.info(f"trip line organizer skipped this id: {parsed_line.id}")
                pass

    return _dict_to_trip_lines(trip_line_dict)


def _dict_to_trip_lines(data: dict[str, Any]) -> TripLines:
    dutyperiods: list[DutyPeriodLines] = []
    for dp in data["duty_periods"]:
        if dp["layover"] is None:
            layover = None
        else:
            layover = LayoverLines(**dp["layover"])
        dutyperiods.append(
            DutyPeriodLines(
                report=dp["report"],
                flights=dp["flights"],
                release=dp["release"],
                layover=layover,
            )
        )
    trip = TripLines(
        page_header_2=data["page_header_2"],
        trip_header=data["trip_header"],
        trip_footer=data["trip_footer"],
        page_footer=data["page_footer"],
        duty_periods=dutyperiods,
    )
    return trip
