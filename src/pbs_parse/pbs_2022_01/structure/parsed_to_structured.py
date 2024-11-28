import logging
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from pfmsoft.state_parser.model import ParsedIndexedString

from pbs_parse.pbs_2022_01.models import parsed_lines_TD as linesTD
from pbs_parse.pbs_2022_01.models import structured
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip, parsed_trip_serializer

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class LayoverLines:
    layover: ParsedIndexedString
    lines: list[ParsedIndexedString] = field(default_factory=list)


@dataclass(slots=True)
class DutyPeriodLines:
    report: ParsedIndexedString
    flights: list[ParsedIndexedString]
    release: ParsedIndexedString
    layover: Optional[LayoverLines]


@dataclass(slots=True)
class TripLines:
    page_header_2: ParsedIndexedString
    trip_header: ParsedIndexedString
    trip_footer: ParsedIndexedString
    page_footer: ParsedIndexedString
    duty_periods: list[DutyPeriodLines] = field(default_factory=list)


def translate_file(
    path_in: Path, effective_from: date, effective_to: date
) -> structured.StructuredTrip:
    parsed_trip = parsed_trip_serializer().load_from_json(path_in=path_in)
    return translate(
        parsed_trip=parsed_trip,
        effective_from=effective_from,
        effective_to=effective_to,
    )


def translate(
    parsed_trip: ParsedTrip, effective_from: date, effective_to: date
) -> structured.StructuredTrip:
    trip_lines = _organize_lines(parsed_trip=parsed_trip)
    calendar = _collect_calendar(parsed_trip=parsed_trip)
    trip = _translate_trip(
        trip_lines=trip_lines,
        calendar=calendar,
        effective_from=effective_from,
        effective_to=effective_to,
        source_uuid=parsed_trip.uuid,
    )
    return trip


def _translate_flight(parsed_data: linesTD.Flight, idx: int) -> structured.Flight:
    flight = structured.Flight(
        uuid=str(uuid4()),
        idx=str(idx),
        dutyperiod_idx=parsed_data["dutyperiod_idx"],
        dep_arr_day=parsed_data["dep_arr_day"],
        eq_code=parsed_data["eq_code"],
        flight_number=parsed_data["flight_number"],
        deadhead=parsed_data["deadhead"],
        deadhead_code=parsed_data["deadhead_code"],
        departure_station=parsed_data["departure_station"],
        departure_time=parsed_data["departure_time"],
        crew_meal=parsed_data["crew_meal"],
        arrival_station=parsed_data["arrival_station"],
        arrival_time=parsed_data["arrival_time"],
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
        uuid=str(uuid4()),
        idx=str(idx),
        report_time=dutyperiod_lines.report.data["report"],
        release_time=dutyperiod_lines.release.data["release"],
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
        uuid=str(uuid4()),
        rest=layover_lines.layover.data["rest"],
        city=layover_lines.layover.data["layover_city"],
        hotels=_translate_hotels(
            layover_lines.lines,
            name=layover_lines.layover.data["name"],
            phone=layover_lines.layover.data["phone"],
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
    trip_lines: TripLines,
    calendar: list[str],
    effective_from: date,
    effective_to: date,
    source_uuid: str,
) -> structured.StructuredTrip:
    dutyperiods: list[structured.DutyPeriod] = [
        _translate_dutyperiod(x, idx)
        for idx, x in enumerate(trip_lines.duty_periods, start=1)
    ]
    assert isinstance(effective_from, date)
    external = structured.ExternalData(
        effective_from=effective_from.isoformat(),
        effective_to=effective_to.isoformat(),
    )
    page_header = structured.PageHeader(
        from_date=trip_lines.page_header_2.data["from_date"],
        to_date=trip_lines.page_header_2.data["to_date"],
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
    trip = structured.StructuredTrip(
        source=source_uuid,
        number=trip_lines.trip_header.data["number"],
        ops_count=trip_lines.trip_header.data["ops_count"],
        positions=trip_lines.trip_header.data["positions"],
        operations=trip_lines.trip_header.data["operations"],
        qualifications=trip_lines.trip_header.data["qualifications"],
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
        maybe = parsed_line.data.get("calendar", [])
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
