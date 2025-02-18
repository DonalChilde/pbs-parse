"""Data model for a `Trip`."""

from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict

from pbs_parse.airports import airport_from_iata
from pbs_parse.pbs_2022_01.models.bid_data import BidData

from ...snippets.whenever.pydantic import PydanticTimeDelta, PydanticZonedDateTime

UTC = ZoneInfo("UTC")


class Position(BaseModel):
    """A position, eg. CA or FO."""

    name: str


class AirportInfo(BaseModel):
    """Airport/city identifiers."""

    iata: str
    icao: str
    tz_name: str

    def __str__(self) -> str:
        """__str__.

        Returns:
            str: _description_
        """
        return (
            f"AirportInfo:\n"
            f"{'iata:':>12} {self.iata}\n"
            f"{'icao:':>12} {self.icao}\n"
            f"{'tz_name:':>12} {self.tz_name}\n"
        )


class BaseEquipment(BaseModel):
    """Base and equipment in the bidding context."""

    base: AirportInfo
    satellite_base: AirportInfo | None
    equipment: str


class Operation(BaseModel):
    """An area of operation."""

    name: str


class Flight(BaseModel):
    """A flight."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    eq_code: str
    number: str
    departure_station: AirportInfo
    departure: PydanticZonedDateTime
    arrival_station: AirportInfo
    arrival: PydanticZonedDateTime
    deadhead: bool
    deadhead_code: str
    crewmeal: str
    eq_change: bool
    flight_time: PydanticTimeDelta
    operating_time: PydanticTimeDelta
    soft_time: PydanticTimeDelta
    ground_time: PydanticTimeDelta

    def __str__(self) -> str:
        """__str__.

        Returns:
            str: _description_
        """
        return (
            f"{f'Flight:':>14} {self.number} equip: {self.eq_code} DH: {self.deadhead}\n"
            # f"{'utc:':>38} {self.departure_utc}{f'utc:':>18} {self.arrival_utc} BLOCK: {format_td(self.arrival_utc - self.departure_utc)}\n"
            f"{f'Depart {self.departure_station.iata} BLOCK: {self.flight_time} lcl:':>38} {self.departure}{f'Arrive {self.arrival_station.iata} lcl:':>18} {self.arrival} BLOCK: {self.arrival - self.departure}\n"
            # f"{'hbt:':>38} {self.departure_hbt}{f'hbt:':>18} {self.arrival_hbt} BLOCK: {format_td(self.arrival_hbt - self.departure_hbt)}\n"
            f"{'flight:':>38} {self.flight_time} soft: {self.soft_time} operating: {self.operating_time} ground: {self.ground_time}\n"
            f"{' ' * 14}{self!r}\n"
        )


class Transportation(BaseModel):
    """Transpo."""

    name: str
    phone: str


class Hotel(BaseModel):
    """A Hotel."""

    name: str
    phone: str
    transportation: list[Transportation]


class Layover(BaseModel):
    """A Layover."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    layover_station: AirportInfo
    start: PydanticZonedDateTime
    end: PydanticZonedDateTime
    rest: PydanticTimeDelta
    hotels: list[Hotel]

    def __str__(self) -> str:
        """__str__."""
        return (
            # f"{'utc:':>35} {self.start_utc}{f'utc:':>18} {self.end_utc} REST: {format_td(self.end_utc - self.start_utc)}\n"
            f"{f'Layover {self.layover_station.iata} REST: {self.rest} lcl:':>35} {self.start}{f'End lcl:':>18} {self.end} REST: {self.end - self.start}\n"
            # f"{'hbt:':>35} {self.start_hbt}{f'hbt:':>18} {self.end_hbt} REST: {format_td(self.end_hbt - self.start_hbt)}\n"
            f"{' ' * 14}{self!r}\n"
        )


class DutyPeriod(BaseModel):
    """A dutyperiod."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    report_station: AirportInfo
    report: PydanticZonedDateTime
    release_station: AirportInfo
    release: PydanticZonedDateTime
    duty: PydanticTimeDelta
    flight_duty: PydanticTimeDelta
    operating_time: PydanticTimeDelta
    flight_time: PydanticTimeDelta
    soft_time: PydanticTimeDelta
    layover: Layover | None
    flights: list[Flight]

    def __str__(self) -> str:
        """__str__.

        Returns:
            str: _description_
        """
        return (
            # f"{'utc:':>30} {self.report_utc}{f'utc:':>18} {self.release_utc} DUTY: {format_td(self.release_utc - self.report_utc)}\n"
            f"{f'Report {self.report_station.iata} DUTY: {self.duty} lcl:':>30} {self.report}{f'Release {self.release_station.iata} lcl:':>18} {self.release} DUTY: {self.release - self.report}\n"
            # f"{'hbt:':>30} {self.report_hbt}{f'hbt:':>18} {self.release_hbt} DUTY: {format_td(self.release_hbt - self.report_hbt)}\n"
            "\n"
            "       FLIGHTS\n"
            f"{'\n'.join([str(x) for x in self.flights])}"
            "\n"
            f"{f'       LAYOVER\n{self.layover}' if self.layover is not None else ''}"
        )


class ExpandedTripSource(BaseModel):
    """StructuredTripSource."""

    txt_file: str = "TXT_FILE"
    page_lines: str = "PAGE_LINES"
    trip_lines: str = "TRIP_LINES"
    parsed_trip: str = "PARSED_TRIP"


class ExpandedTrip(BaseModel):
    """A trip."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    source: ExpandedTripSource
    bid: BidData
    trip_number: str
    base_equipment: BaseEquipment
    special_qual: bool
    start_station: AirportInfo
    start: PydanticZonedDateTime
    end_station: AirportInfo
    end: PydanticZonedDateTime
    flight_time: PydanticTimeDelta
    operating_time: PydanticTimeDelta
    soft_time: PydanticTimeDelta
    tafb: PydanticTimeDelta
    dutyperiods: list[DutyPeriod]
    positions: list[Position]
    operations: list[Operation]
    errors: list[str] = []

    def default_file_name(self) -> str:
        """Assemble a file name from trip data."""
        name = (
            "expanded-trip"
            f"_{self.bid.name}"
            f"_{self.base_equipment.base.iata}"
            f"{f'_{self.base_equipment.satellite_base.iata}' if self.base_equipment.satellite_base is not None else ''}"
            f"_{self.base_equipment.equipment}"
            f"_{self.start.date().format_common_iso()}"
            f"_{self.trip_number}"
            ".json"
        )

        return name

    def __str__(self) -> str:
        """__str__."""
        return (
            f"EXPANDED TRIP {self.trip_number}-{self.start.date()} {self.base_equipment!r}\n\n"
            f"SOURCE: {self.source!r}\n"
            f"ERRORS: {len(self.errors)}\n"
            f"{'\n'.join([f'  {x}' for x in self.errors])}\n"
            f"\n\n"
            f"Positions: {' '.join([x.name for x in self.positions])} "
            f"SpecialQual: {self.special_qual} "
            f"Operations: {' '.join([x.name for x in self.operations])}\n\n"
            # f"{'utc:':>30} {self.start_utc}{f'utc:':>18} {self.end_utc} TAFB: {format_td(self.end_utc - self.start_utc)}\n"
            f"{f'Start {self.start_station.iata} TAFB: {self.tafb} lcl:':>30} {self.start}{f'End {self.end_station.iata} lcl:':>18} {self.end} TAFB: {self.end - self.start}\n"
            # f"{'hbt:':>30} {self.start_hbt}{f'hbt:':>18} {self.end_hbt} TAFB: {format_td(self.end_hbt - self.start_hbt)}\n"
            "\n"
            "DUTYPERIODS\n"
            f"{'\n'.join([str(x) for x in self.dutyperiods])}\n"
            f"{'\n'.join([str(x) for x in airports_in_trip(self).values()])}"
        )


def airports_in_trip(expanded: ExpandedTrip) -> dict[str, AirportInfo]:
    """airports_in_trip.

    Args:
        expanded (ExpandedTrip): _description_

    Returns:
        dict[str, AirportInfo]: _description_
    """
    airports: dict[str, AirportInfo] = {}
    airports[expanded.start_station.iata] = expanded.start_station
    airports[expanded.end_station.iata] = expanded.end_station
    for dp in expanded.dutyperiods:
        airports[dp.report_station.iata] = dp.report_station
        airports[dp.release_station.iata] = dp.release_station
        if dp.layover is not None:
            airports[dp.layover.layover_station.iata] = dp.layover.layover_station
        for flight in dp.flights:
            airports[flight.departure_station.iata] = flight.departure_station
            airports[flight.arrival_station.iata] = flight.arrival_station
    return airports


def get_airport_code_from_iata(iata: str) -> AirportInfo:
    """Get airport info from database."""
    airport = airport_from_iata(iata=iata)
    return AirportInfo(
        iata=airport["iata"], icao=airport["icao"], tz_name=airport["tz"]
    )
