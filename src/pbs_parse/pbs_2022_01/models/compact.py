from dataclasses import dataclass


@dataclass
class Hotel:
    name: str
    phone: str


@dataclass
class Transportation:
    name: str
    phone: str


@dataclass
class HotelInfo:
    hotel: Hotel
    transportation: list[Transportation]


@dataclass
class LclHbt:
    lcl: str
    hbt: str


@dataclass
class Layover:
    uuid: str
    odl: str
    city: str
    hotel_info: list[HotelInfo]


@dataclass
class Flight:
    uuid: str
    dp_idx: str
    idx: str
    dep_arr_day: str
    eq_code: str
    number: str
    deadhead: bool
    departure_station: str
    departure: LclHbt
    meal: str
    arrival_station: str
    arrival: LclHbt
    block: str
    synth: str
    ground: str
    equipment_change: str


@dataclass
class DutyPeriod:
    uuid: str
    idx: str
    report: LclHbt
    report_station: str
    release: LclHbt
    release_station: str
    block: str
    synth: str
    total_pay: str
    duty: str
    flight_duty: str
    layover: Layover | None
    flights: list[Flight]


@dataclass
class Trip:
    uuid: str
    number: str
    positions: list[str]
    operations: str
    qualifications: str
    block: str
    synth: str
    total_pay: str
    tafb: str
    dutyperiods: list[DutyPeriod]
    start_calendar: list[str]
