"""Trip as simple objects."""

from typing import TypedDict


class Position(TypedDict):
    """A position, eg. CA or FO."""

    name: str


class AirportCode(TypedDict):
    """Airport/city identifiers."""

    iata: str
    icao: str
    tz_name: str


class BaseEquipment(TypedDict):
    """Base and equipment in the bidding context."""

    base: AirportCode
    satellite_base: AirportCode | None
    equipment: str


class Operation(TypedDict):
    """An area of operation."""

    name: str


class Flight(TypedDict):
    """A flight."""

    eq_code: str
    number: str
    departure_station: AirportCode
    departure_utc: str
    arrival_station: AirportCode
    arrival_utc: str
    deadhead: bool
    deadhead_code: str
    crewmeal: str
    eq_change: bool
    flight_time: str
    operating_time: str
    soft_time: str
    ground_time: str


class Transportation(TypedDict):
    """Transpo."""

    name: str
    phone: str


class Hotel(TypedDict):
    """A Hotel."""

    name: str
    phone: str
    trans: list[Transportation]


class Layover(TypedDict):
    """A Layover."""

    layover_station: AirportCode
    start_utc: str
    end_utc: str
    hotels: list[Hotel]
    rest: str


class DutyPeriod(TypedDict):
    """A dutyperiod."""

    report_station: AirportCode
    report_utc: str
    release_station: AirportCode
    release_utc: str
    flights: list[Flight]
    duty: str
    flight_duty: str
    operating_time: str
    flight_time: str
    soft_time: str
    layover: Layover | None


class ExpandedTrip(TypedDict):
    """A trip."""

    source: str
    trip_number: str
    base_equipment: BaseEquipment
    positions: list[Position]
    operations: list[Operation]
    special_qual: bool
    start_station: AirportCode
    start_utc: str
    end_station: AirportCode
    end_utc: str
    flight_time: str
    operating_time: str
    soft_time: str
    tafb: str
    dutyperiods: list[DutyPeriod]
