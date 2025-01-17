"""Structured model of a parsed trip as TypedDict, no translations from strings.

This can be used to represent imported json data, usually before conversion to the dataclass version.
"""

# ruff: noqa: D101
from typing import TypedDict


class MonthDay(TypedDict):
    month: str
    day: str


class DualTime(TypedDict):
    lcl: str
    hbt: str


class Transportation(TypedDict):
    name: str
    phone: str


class Hotel(TypedDict):
    name: str
    phone: str
    transportation: list[Transportation]


class Layover(TypedDict):
    rest: str
    city: str
    hotels: list[Hotel]


class Flight(TypedDict):
    dutyperiod_idx: str
    idx: str
    depart_day: str
    arrive_day: str
    equipment_code: str
    flight_number: str
    deadhead: bool
    deadhead_code: str
    departure_station: str
    departure_time: DualTime
    crew_meal: str
    arrival_station: str
    arrival_time: DualTime
    block: str
    synth: str
    ground: str
    equipment_change: bool


class DutyPeriod(TypedDict):
    idx: str
    report_time: DualTime
    release_time: DualTime
    block: str
    synth: str
    total_pay: str
    duty: str
    flight_duty: str
    layover: Layover | None
    flights: list[Flight]


class PageHeader(TypedDict):
    from_date: MonthDay
    to_date: MonthDay


class PageFooter(TypedDict):
    issued: str
    effective: str
    base: str
    satellite_base: str
    equipment: str
    division: str
    page: str


class ExternalData(TypedDict):
    effective_from: str
    effective_to: str


class StructuredTripSourceTD(TypedDict):
    txt_file: str
    page_lines: str
    trip_lines: str
    parsed_trip: str


class StructuredTripTD(TypedDict):
    source: StructuredTripSourceTD
    uuid: str
    source_uuid: str
    idx: str
    number: str
    ops_count: str
    block: str
    synth: str
    total_pay: str
    tafb: str
    external: ExternalData
    page_header: PageHeader
    page_footer: PageFooter
    positions: list[str]
    operations: list[str]
    special_qual: bool
    dutyperiods: list[DutyPeriod]
    calendar: list[str]
