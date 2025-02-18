"""Trip as simple objects."""

from typing import TypedDict

from pbs_parse.pbs_2022_01.models.bid_data_td import BidDataTD


class Position(TypedDict):
    """A position, eg. CA or FO."""

    name: str


class AirportInfo(TypedDict):
    """Airport/city identifiers."""

    iata: str
    icao: str
    tz_name: str


class BaseEquipment(TypedDict):
    """Base and equipment in the bidding context."""

    base: AirportInfo
    satellite_base: AirportInfo | None
    equipment: str


class Operation(TypedDict):
    """An area of operation."""

    name: str


class Flight(TypedDict):
    """A flight."""

    eq_code: str
    number: str
    departure_station: AirportInfo
    departure: str
    arrival_station: AirportInfo
    arrival: str
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
    transportation: list[Transportation]


class Layover(TypedDict):
    """A Layover."""

    layover_station: AirportInfo
    start: str
    end: str
    hotels: list[Hotel]
    rest: str


class DutyPeriod(TypedDict):
    """A dutyperiod."""

    report_station: AirportInfo
    report: str
    release_station: AirportInfo
    release: str
    flights: list[Flight]
    duty: str
    flight_duty: str
    operating_time: str
    flight_time: str
    soft_time: str
    layover: Layover | None


class ExpandedTripSourceTD(TypedDict):
    """ExpandedTripSource."""

    txt_file: str
    page_lines: str
    trip_lines: str
    parsed_trip: str


class ExpandedTripTD(TypedDict):
    """A trip."""

    source: ExpandedTripSourceTD
    bid: BidDataTD
    trip_number: str
    base_equipment: BaseEquipment
    positions: list[Position]
    operations: list[Operation]
    special_qual: bool
    start_station: AirportInfo
    start: str
    end_station: AirportInfo
    end: str
    flight_time: str
    operating_time: str
    soft_time: str
    tafb: str
    dutyperiods: list[DutyPeriod]
    errors: list[str]
