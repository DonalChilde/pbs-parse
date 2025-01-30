"""Data model for a `Trip`."""

from dataclasses import dataclass, field
from pathlib import Path
from uuid import NAMESPACE_DNS, uuid5
from zoneinfo import ZoneInfo

from pfmsoft.simple_serializer import DataclassSerializer
from whenever import TimeDelta, ZonedDateTime

import pbs_parse.pbs_2022_01.models.expanded_TD as TD
from pbs_parse.airports import airport_from_iata
from pbs_parse.pbs_2022_01.models.bid_data import BidData
from pbs_parse.snippets.file.data_file_loader import DataFileLoader

UTC = ZoneInfo("UTC")
TRIP_NS = uuid5(NAMESPACE_DNS, "pbs_parse.pbs_2022_01.trip")


@dataclass(slots=True, kw_only=True)
class Position:
    """A position, eg. CA or FO."""

    name: str


@dataclass(slots=True, kw_only=True)
class AirportInfo:
    """Airport/city identifiers."""

    iata: str
    icao: str
    tz_name: str

    def to_simple(self) -> TD.AirportInfo:
        """AirportCode to simple."""
        result = TD.AirportInfo(iata=self.iata, icao=self.icao, tz_name=self.tz_name)
        return result

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


@dataclass(slots=True, kw_only=True)
class BaseEquipment:
    """Base and equipment in the bidding context."""

    base: AirportInfo
    satellite_base: AirportInfo | None
    equipment: str

    def to_simple(self) -> TD.BaseEquipment:
        """BaseEquipment to simple."""
        if self.satellite_base is None:
            satellite_base = None
        else:
            satellite_base = self.satellite_base.to_simple()
        result = TD.BaseEquipment(
            base=self.base.to_simple(),
            satellite_base=satellite_base,
            equipment=self.equipment,
        )
        return result

    @staticmethod
    def from_simple(simple_obj: TD.BaseEquipment) -> "BaseEquipment":
        """BaseEquipment from simple object."""
        if simple_obj["satellite_base"] is None:
            satellite_base = None
        else:
            satellite_base = AirportInfo(**simple_obj["satellite_base"])
        result = BaseEquipment(
            base=AirportInfo(**simple_obj["base"]),
            satellite_base=satellite_base,
            equipment=simple_obj["equipment"],
        )
        return result


@dataclass(slots=True, kw_only=True)
class Operation:
    """An area of operation."""

    name: str


@dataclass(slots=True, kw_only=True)
class Flight:
    """A flight."""

    eq_code: str
    number: str
    departure_station: AirportInfo
    departure: ZonedDateTime
    arrival_station: AirportInfo
    arrival: ZonedDateTime
    deadhead: bool
    deadhead_code: str
    crewmeal: str
    eq_change: bool
    flight_time: TimeDelta
    operating_time: TimeDelta
    soft_time: TimeDelta
    ground_time: TimeDelta

    def to_simple(self) -> TD.Flight:
        """Flight to simple."""
        result = TD.Flight(
            eq_code=self.eq_code,
            number=self.number,
            departure_station=self.departure_station.to_simple(),
            departure=self.departure.format_common_iso(),
            arrival_station=self.arrival_station.to_simple(),
            arrival=self.arrival.format_common_iso(),
            deadhead=self.deadhead,
            deadhead_code=self.deadhead_code,
            crewmeal=self.crewmeal,
            eq_change=self.eq_change,
            flight_time=self.flight_time.format_common_iso(),
            operating_time=self.operating_time.format_common_iso(),
            soft_time=self.soft_time.format_common_iso(),
            ground_time=self.ground_time.format_common_iso(),
        )

        return result

    @staticmethod
    def from_simple(simple_obj: TD.Flight) -> "Flight":
        """Flight from simple."""
        result = Flight(
            eq_code=simple_obj["eq_code"],
            number=simple_obj["number"],
            departure_station=AirportInfo(**simple_obj["departure_station"]),
            departure=ZonedDateTime.parse_common_iso(simple_obj["departure"]),
            arrival_station=AirportInfo(**simple_obj["arrival_station"]),
            arrival=ZonedDateTime.parse_common_iso(simple_obj["arrival"]),
            deadhead=simple_obj["deadhead"],
            deadhead_code=simple_obj["deadhead_code"],
            crewmeal=simple_obj["crewmeal"],
            eq_change=simple_obj["eq_change"],
            flight_time=TimeDelta.parse_common_iso(simple_obj["flight_time"]),
            operating_time=TimeDelta.parse_common_iso(simple_obj["operating_time"]),
            soft_time=TimeDelta.parse_common_iso(simple_obj["soft_time"]),
            ground_time=TimeDelta.parse_common_iso(simple_obj["ground_time"]),
        )
        return result

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


@dataclass(slots=True, kw_only=True)
class Transportation:
    """Transpo."""

    name: str
    phone: str


@dataclass(slots=True, kw_only=True)
class Hotel:
    """A Hotel."""

    name: str
    phone: str
    transportation: list[Transportation]

    def to_simple(self) -> TD.Hotel:
        """Hotel to simple."""
        result = TD.Hotel(
            name=self.name,
            phone=self.phone,
            transportation=[
                TD.Transportation(name=x.name, phone=x.phone)
                for x in self.transportation
            ],
        )
        return result

    @staticmethod
    def from_simple(simple_obj: TD.Hotel) -> "Hotel":
        """Hotel from simple."""
        result = Hotel(
            name=simple_obj["name"],
            phone=simple_obj["phone"],
            transportation=[Transportation(**x) for x in simple_obj["transportation"]],
        )
        return result


@dataclass(slots=True, kw_only=True)
class Layover:
    """A Layover."""

    layover_station: AirportInfo
    start: ZonedDateTime
    end: ZonedDateTime
    rest: TimeDelta
    hotels: list[Hotel] = field(default_factory=list)

    def __str__(self) -> str:
        """__str__."""
        return (
            # f"{'utc:':>35} {self.start_utc}{f'utc:':>18} {self.end_utc} REST: {format_td(self.end_utc - self.start_utc)}\n"
            f"{f'Layover {self.layover_station.iata} REST: {self.rest} lcl:':>35} {self.start}{f'End lcl:':>18} {self.end} REST: {self.end - self.start}\n"
            # f"{'hbt:':>35} {self.start_hbt}{f'hbt:':>18} {self.end_hbt} REST: {format_td(self.end_hbt - self.start_hbt)}\n"
            f"{' ' * 14}{self!r}\n"
        )

    def to_simple(self) -> TD.Layover:
        """Layover to simple."""
        result = TD.Layover(
            layover_station=self.layover_station.to_simple(),
            start=self.start.format_common_iso(),
            end=self.end.format_common_iso(),
            hotels=[x.to_simple() for x in self.hotels],
            rest=self.rest.format_common_iso(),
        )
        return result

    @staticmethod
    def from_simple(simple_obj: TD.Layover) -> "Layover":
        """Layover from simple."""
        result = Layover(
            layover_station=AirportInfo(**simple_obj["layover_station"]),
            start=ZonedDateTime.parse_common_iso(simple_obj["start"]),
            end=ZonedDateTime.parse_common_iso(simple_obj["end"]),
            hotels=[Hotel.from_simple(x) for x in simple_obj["hotels"]],
            rest=TimeDelta.parse_common_iso(simple_obj["rest"]),
        )
        return result


@dataclass(slots=True, kw_only=True)
class DutyPeriod:
    """A dutyperiod."""

    report_station: AirportInfo
    report: ZonedDateTime
    release_station: AirportInfo
    release: ZonedDateTime
    duty: TimeDelta
    flight_duty: TimeDelta
    operating_time: TimeDelta
    flight_time: TimeDelta
    soft_time: TimeDelta
    layover: Layover | None
    flights: list[Flight] = field(default_factory=list)

    def to_simple(self) -> TD.DutyPeriod:
        """DutyPeriod to simple."""
        if self.layover is None:
            layover = None
        else:
            layover = self.layover.to_simple()
        result = TD.DutyPeriod(
            report_station=self.report_station.to_simple(),
            report=self.report.format_common_iso(),
            release_station=self.release_station.to_simple(),
            release=self.release.format_common_iso(),
            flights=[x.to_simple() for x in self.flights],
            duty=self.duty.format_common_iso(),
            flight_duty=self.flight_duty.format_common_iso(),
            operating_time=self.operating_time.format_common_iso(),
            flight_time=self.operating_time.format_common_iso(),
            soft_time=self.soft_time.format_common_iso(),
            layover=layover,
        )
        return result

    @staticmethod
    def from_simple(simple_obj: TD.DutyPeriod) -> "DutyPeriod":
        """Dutyperiod from simple."""
        if simple_obj["layover"] is None:
            layover = None
        else:
            layover = Layover.from_simple(simple_obj["layover"])
        result = DutyPeriod(
            report_station=AirportInfo(**simple_obj["report_station"]),
            report=ZonedDateTime.parse_common_iso(simple_obj["report"]),
            release_station=AirportInfo(**simple_obj["release_station"]),
            release=ZonedDateTime.parse_common_iso(simple_obj["release"]),
            flights=[Flight.from_simple(x) for x in simple_obj["flights"]],
            duty=TimeDelta.parse_common_iso(simple_obj["duty"]),
            flight_duty=TimeDelta.parse_common_iso(simple_obj["flight_duty"]),
            operating_time=TimeDelta.parse_common_iso(simple_obj["operating_time"]),
            flight_time=TimeDelta.parse_common_iso(simple_obj["flight_time"]),
            soft_time=TimeDelta.parse_common_iso(simple_obj["soft_time"]),
            layover=layover,
        )
        return result

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


@dataclass(slots=True)
class ExpandedTripSource:
    """StructuredTripSource."""

    txt_file: str = "TXT_FILE"
    page_lines: str = "PAGE_LINES"
    trip_lines: str = "TRIP_LINES"
    parsed_trip: str = "PARSED_TRIP"

    def to_simple(self) -> TD.ExpandedTripSourceTD:
        """Turn into simple object."""
        return TD.ExpandedTripSourceTD(
            txt_file=self.txt_file,
            page_lines=self.page_lines,
            trip_lines=self.trip_lines,
            parsed_trip=self.parsed_trip,
        )


@dataclass(slots=True, kw_only=True)
class ExpandedTrip:
    """A trip."""

    source: ExpandedTripSource
    bid: BidData
    trip_number: str
    base_equipment: BaseEquipment
    special_qual: bool
    start_station: AirportInfo
    start: ZonedDateTime
    end_station: AirportInfo
    end: ZonedDateTime
    flight_time: TimeDelta
    operating_time: TimeDelta
    soft_time: TimeDelta
    tafb: TimeDelta
    dutyperiods: list[DutyPeriod] = field(default_factory=list)
    positions: list[Position] = field(default_factory=list)
    operations: list[Operation] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

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

    @staticmethod
    def from_simple(simple_obj: TD.ExpandedTripTD) -> "ExpandedTrip":
        """Turn simple object into Trip."""
        result = ExpandedTrip(
            source=ExpandedTripSource(**simple_obj["source"]),
            bid=BidData.from_simple(simple_obj["bid"]),
            trip_number=simple_obj["trip_number"],
            base_equipment=BaseEquipment.from_simple(simple_obj["base_equipment"]),
            positions=[Position(name=x["name"]) for x in simple_obj["positions"]],
            operations=[Operation(name=x["name"]) for x in simple_obj["operations"]],
            special_qual=simple_obj["special_qual"],
            start_station=AirportInfo(**simple_obj["start_station"]),
            start=ZonedDateTime.parse_common_iso(simple_obj["start"]),
            end_station=AirportInfo(**simple_obj["end_station"]),
            end=ZonedDateTime.parse_common_iso(simple_obj["end"]),
            flight_time=TimeDelta.parse_common_iso(simple_obj["flight_time"]),
            operating_time=TimeDelta.parse_common_iso(simple_obj["operating_time"]),
            soft_time=TimeDelta.parse_common_iso(simple_obj["soft_time"]),
            tafb=TimeDelta.parse_common_iso(simple_obj["tafb"]),
            dutyperiods=[DutyPeriod.from_simple(x) for x in simple_obj["dutyperiods"]],
            errors=[x for x in simple_obj["errors"]],
        )
        return result

    def to_simple(self) -> TD.ExpandedTripTD:
        """Trip to simple object."""
        result = TD.ExpandedTripTD(
            source=self.source.to_simple(),
            bid=self.bid.to_simple(),
            trip_number=self.trip_number,
            base_equipment=self.base_equipment.to_simple(),
            positions=[TD.Position(name=x.name) for x in self.positions],
            operations=[TD.Operation(name=x.name) for x in self.operations],
            special_qual=self.special_qual,
            start_station=self.start_station.to_simple(),
            start=self.start.format_common_iso(),
            end_station=self.end_station.to_simple(),
            end=self.end.format_common_iso(),
            flight_time=self.flight_time.format_common_iso(),
            operating_time=self.operating_time.format_common_iso(),
            soft_time=self.soft_time.format_common_iso(),
            tafb=self.tafb.format_common_iso(),
            dutyperiods=[x.to_simple() for x in self.dutyperiods],
            errors=[x for x in self.errors],
        )
        return result


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


def trip_serializer() -> DataclassSerializer[ExpandedTrip, TD.ExpandedTripTD]:
    """Init a Trip serializer.

    Returns:
        DataclassSerializer[Trip, TD.Trip]: _description_
    """
    return DataclassSerializer[ExpandedTrip, TD.ExpandedTripTD](
        complex_factory=ExpandedTrip.from_simple, simple_factory=ExpandedTrip.to_simple
    )


EXPANDED_TRIP_SERIALIZER = trip_serializer()


class ExpandedTripSaver:
    """ExpandedTripSaver."""

    def __init__(self, path_out: Path) -> None:
        """Save ExpandedTrip to a directory using the default file name.

        Args:
            path_out (Path): The directory to save the ExpandedTrip to.
        """
        if path_out.is_file():
            raise ValueError(
                f"Path out is an existing file, should be a directory. {path_out=}"
            )
        self.path_out = path_out

    def __call__(self, expanded_trip: ExpandedTrip, overwrite: bool = False) -> Path:
        """Save ExpandedTrip to a directory using the default file name.

        Args:
            expanded_trip (ExpandedTrip): The ExpandedTrip to save.
            overwrite (bool): Overwrite existing files.

        Returns:
            Path: The path to the saved file.
        """
        path_out = self.path_out / expanded_trip.default_file_name()
        EXPANDED_TRIP_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=expanded_trip, overwrite=overwrite
        )
        return path_out


class ExpandedTripLoader(DataFileLoader[ExpandedTrip]):
    """ExpandedTripLoader."""

    def __init__(self, path_in: Path, glob: str = "expanded-trip_*.json") -> None:
        """Load ExpandedTrip from directory.

        Args:
            path_in (Path): The directory to load files from.
            glob (str, optional): The glob to match files. Defaults to "expanded-trip_*.json".
        """
        super().__init__(path_in, glob)

    def _translate(self, obj_path: Path) -> ExpandedTrip:
        return EXPANDED_TRIP_SERIALIZER.load_from_json(path_in=obj_path)
