"""
Structured model of a parsed trip as TypedDict, no translations from strings.

This can be used to represent imported json data, usually before conversion to the dataclass version.
"""

from typing import TypedDict


class Transportation(TypedDict):
    name: str
    phone: str


class Hotel(TypedDict):
    name: str
    phone: str
    transportation: list[Transportation]


class Layover(TypedDict):
    uuid: str
    rest: str
    city: str
    hotels: list[Hotel]


class Flight(TypedDict):
    uuid: str
    dutyperiod_idx: str
    idx: str
    dep_arr_day: str
    eq_code: str
    flight_number: str
    deadhead: str
    deadhead_code: str
    departure_station: str
    departure_time: str
    crew_meal: str
    arrival_station: str
    arrival_time: str
    block: str
    synth: str
    ground: str
    equipment_change: str


class DutyPeriod(TypedDict):
    uuid: str
    idx: str
    report_time: str
    release_time: str
    block: str
    synth: str
    total_pay: str
    duty: str
    flight_duty: str
    layover: Layover | None
    flights: list[Flight]


class PageHeader(TypedDict):
    from_date: str
    to_date: str


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


class StructuredTripTD(TypedDict):
    uuid: str
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
    qualifications: list[str]
    dutyperiods: list[DutyPeriod]
    calendar: list[str]
