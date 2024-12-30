"""Data model for a `Trip`."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from uuid import NAMESPACE_DNS, UUID, uuid5
from zoneinfo import ZoneInfo

from pfmsoft.simple_serializer import DataclassSerializer

import pbs_parse.pbs_2022_01.models.expanded_TD as TD
from pbs_parse.airports import airport_from_iata
from pbs_parse.snippets.datetime.iso8601_duration import (
    string_to_timedelta,
    timedelta_to_isoformat,
)
from pbs_parse.snippets.file.data_file_loader import DataFileLoader

UTC = ZoneInfo("UTC")
TRIP_NS = uuid5(NAMESPACE_DNS, "pbs_parse.pbs_2022_01.trip")


@dataclass(slots=True, kw_only=True)
class Position:
    """A position, eg. CA or FO."""

    name: str


@dataclass(slots=True, kw_only=True)
class AirportCode:
    """Airport/city identifiers."""

    iata: str
    icao: str
    tz_name: str

    def to_simple(self) -> TD.AirportCode:
        """AirportCode to simple."""
        result = TD.AirportCode(iata=self.iata, icao=self.icao, tz_name=self.tz_name)
        return result


@dataclass(slots=True, kw_only=True)
class BaseEquipment:
    """Base and equipment in the bidding context."""

    base: AirportCode
    satellite_base: AirportCode | None
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
            satellite_base = AirportCode(**simple_obj["satellite_base"])
        result = BaseEquipment(
            base=AirportCode(**simple_obj["base"]),
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
    departure_station: AirportCode
    departure_utc: datetime
    departure_lcl: datetime
    departure_hbt: datetime
    arrival_station: AirportCode
    arrival_utc: datetime
    arrival_lcl: datetime
    arrival_hbt: datetime
    deadhead: bool
    deadhead_code: str
    crewmeal: str
    eq_change: bool
    flight_time: timedelta
    operating_time: timedelta
    soft_time: timedelta
    ground_time: timedelta

    def to_simple(self) -> TD.Flight:
        """Flight to simple."""
        result = TD.Flight(
            eq_code=self.eq_code,
            number=self.number,
            departure_station=self.departure_station.to_simple(),
            departure_utc=self.departure_utc.isoformat(),
            departure_lcl=self.departure_lcl.isoformat(),
            departure_hbt=self.departure_hbt.isoformat(),
            arrival_station=self.arrival_station.to_simple(),
            arrival_utc=self.arrival_utc.isoformat(),
            arrival_lcl=self.arrival_lcl.isoformat(),
            arrival_hbt=self.arrival_hbt.isoformat(),
            deadhead=self.deadhead,
            deadhead_code=self.deadhead_code,
            crewmeal=self.crewmeal,
            eq_change=self.eq_change,
            flight_time=timedelta_to_isoformat(self.flight_time),
            operating_time=timedelta_to_isoformat(self.operating_time),
            soft_time=timedelta_to_isoformat(self.soft_time),
            ground_time=timedelta_to_isoformat(self.ground_time),
        )

        return result

    @staticmethod
    def from_simple(simple_obj: TD.Flight) -> "Flight":
        """Flight from simple."""
        result = Flight(
            eq_code=simple_obj["eq_code"],
            number=simple_obj["number"],
            departure_station=AirportCode(**simple_obj["departure_station"]),
            departure_utc=datetime.fromisoformat(
                simple_obj["departure_utc"]
            ).astimezone(UTC),
            departure_lcl=datetime.fromisoformat(simple_obj["departure_lcl"]),
            departure_hbt=datetime.fromisoformat(simple_obj["departure_hbt"]),
            arrival_station=AirportCode(**simple_obj["arrival_station"]),
            arrival_utc=datetime.fromisoformat(simple_obj["arrival_utc"])
            .astimezone(UTC)
            .astimezone(UTC),
            arrival_lcl=datetime.fromisoformat(simple_obj["arrival_lcl"]),
            arrival_hbt=datetime.fromisoformat(simple_obj["arrival_hbt"]),
            deadhead=simple_obj["deadhead"],
            deadhead_code=simple_obj["deadhead_code"],
            crewmeal=simple_obj["crewmeal"],
            eq_change=simple_obj["eq_change"],
            flight_time=string_to_timedelta(simple_obj["flight_time"]),
            operating_time=string_to_timedelta(simple_obj["operating_time"]),
            soft_time=string_to_timedelta(simple_obj["soft_time"]),
            ground_time=string_to_timedelta(simple_obj["ground_time"]),
        )
        return result


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

    layover_station: AirportCode
    start_utc: datetime
    start_lcl: datetime
    start_hbt: datetime
    end_utc: datetime
    end_lcl: datetime
    end_hbt: datetime
    rest: timedelta
    hotels: list[Hotel] = field(default_factory=list)

    def to_simple(self) -> TD.Layover:
        """Layover to simple."""
        result = TD.Layover(
            layover_station=self.layover_station.to_simple(),
            start_utc=self.start_utc.isoformat(),
            start_lcl=self.start_lcl.isoformat(),
            start_hbt=self.start_hbt.isoformat(),
            end_utc=self.end_utc.isoformat(),
            end_lcl=self.end_lcl.isoformat(),
            end_hbt=self.end_hbt.isoformat(),
            hotels=[x.to_simple() for x in self.hotels],
            rest=timedelta_to_isoformat(self.rest),
        )
        return result

    @staticmethod
    def from_simple(simple_obj: TD.Layover) -> "Layover":
        """Layover from simple."""
        result = Layover(
            layover_station=AirportCode(**simple_obj["layover_station"]),
            start_utc=datetime.fromisoformat(simple_obj["start_utc"]).astimezone(UTC),
            start_lcl=datetime.fromisoformat(simple_obj["start_lcl"]),
            start_hbt=datetime.fromisoformat(simple_obj["start_hbt"]),
            end_utc=datetime.fromisoformat(simple_obj["end_utc"]).astimezone(UTC),
            end_lcl=datetime.fromisoformat(simple_obj["end_lcl"]),
            end_hbt=datetime.fromisoformat(simple_obj["end_hbt"]),
            hotels=[Hotel.from_simple(x) for x in simple_obj["hotels"]],
            rest=string_to_timedelta(simple_obj["rest"]),
        )
        return result


@dataclass(slots=True, kw_only=True)
class DutyPeriod:
    """A dutyperiod."""

    report_station: AirportCode
    report_utc: datetime
    report_lcl: datetime
    report_hbt: datetime
    release_station: AirportCode
    release_utc: datetime
    release_lcl: datetime
    release_hbt: datetime
    duty: timedelta
    flight_duty: timedelta
    operating_time: timedelta
    flight_time: timedelta
    soft_time: timedelta
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
            report_utc=self.report_utc.isoformat(),
            report_lcl=self.report_lcl.isoformat(),
            report_hbt=self.report_hbt.isoformat(),
            release_station=self.release_station.to_simple(),
            release_utc=self.release_utc.isoformat(),
            release_lcl=self.release_lcl.isoformat(),
            release_hbt=self.release_hbt.isoformat(),
            flights=[x.to_simple() for x in self.flights],
            duty=timedelta_to_isoformat(self.duty),
            flight_duty=timedelta_to_isoformat(self.flight_duty),
            operating_time=timedelta_to_isoformat(self.operating_time),
            flight_time=timedelta_to_isoformat(self.operating_time),
            soft_time=timedelta_to_isoformat(self.soft_time),
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
            report_station=AirportCode(**simple_obj["report_station"]),
            report_utc=datetime.fromisoformat(simple_obj["report_utc"]).astimezone(UTC),
            report_lcl=datetime.fromisoformat(simple_obj["report_lcl"]),
            report_hbt=datetime.fromisoformat(simple_obj["report_hbt"]),
            release_station=AirportCode(**simple_obj["release_station"]),
            release_utc=datetime.fromisoformat(simple_obj["release_utc"]).astimezone(
                UTC
            ),
            release_lcl=datetime.fromisoformat(simple_obj["release_lcl"]),
            release_hbt=datetime.fromisoformat(simple_obj["release_hbt"]),
            flights=[Flight.from_simple(x) for x in simple_obj["flights"]],
            duty=string_to_timedelta(simple_obj["duty"]),
            flight_duty=string_to_timedelta(simple_obj["flight_duty"]),
            operating_time=string_to_timedelta(simple_obj["operating_time"]),
            flight_time=string_to_timedelta(simple_obj["flight_time"]),
            soft_time=string_to_timedelta(simple_obj["soft_time"]),
            layover=layover,
        )
        return result


@dataclass(slots=True, kw_only=True)
class ExpandedTrip:
    """A trip."""

    source_uuid: str
    source_idx: str
    uuid: str = ""
    trip_number: str
    base_equipment: BaseEquipment
    special_qual: bool
    start_station: AirportCode
    start_utc: datetime
    start_lcl: datetime
    start_hbt: datetime
    end_station: AirportCode
    end_utc: datetime
    end_lcl: datetime
    end_hbt: datetime
    flight_time: timedelta
    operating_time: timedelta
    soft_time: timedelta
    tafb: timedelta
    dutyperiods: list[DutyPeriod] = field(default_factory=list)
    positions: list[Position] = field(default_factory=list)
    operations: list[Operation] = field(default_factory=list)

    def __post_init__(self):
        """Init the uuid if missing, validate if not missing."""
        current_uuid_str = str(self.make_uuid())
        if self.uuid == "":
            self.uuid = current_uuid_str
            return
        if self.uuid != current_uuid_str:
            raise ValueError(
                f"Supplied uuid: {self.uuid} does not match calculated uuid: {current_uuid_str}"
            )

    def make_uuid(self) -> UUID:
        """Make a uuid from a namespace and the source uuid string, start date, and trip number."""
        return uuid5(
            namespace=TRIP_NS,
            name=f"{self.source_uuid}{self.start_utc.isoformat()}{self.trip_number}",
        )

    def default_file_name(self) -> str:
        """Assemble a file name from trip data."""
        ret_value: list[str] = []
        ret_value.append("expanded-trip")
        ret_value.append(f"_{self.source_idx}")
        ret_value.append(f"_{self.start_lcl.date().isoformat()}")
        ret_value.append(f"_{self.base_equipment.base.iata}")
        if self.base_equipment.satellite_base:
            ret_value.append(f"_{self.base_equipment.satellite_base.iata}")
        ret_value.append(f"_{self.base_equipment.equipment}")
        ret_value.append(f"_{self.trip_number}.json")
        return "".join(ret_value)

    @staticmethod
    def from_simple(simple_obj: TD.ExpandedTripTD) -> "ExpandedTrip":
        """Turn simple object into Trip."""
        result = ExpandedTrip(
            source_uuid=simple_obj["source_uuid"],
            source_idx=simple_obj["source_idx"],
            uuid=simple_obj["uuid"],
            trip_number=simple_obj["trip_number"],
            base_equipment=BaseEquipment.from_simple(simple_obj["base_equipment"]),
            positions=[Position(name=x["name"]) for x in simple_obj["positions"]],
            operations=[Operation(name=x["name"]) for x in simple_obj["operations"]],
            special_qual=simple_obj["special_qual"],
            start_station=AirportCode(**simple_obj["start_station"]),
            start_utc=datetime.fromisoformat(simple_obj["start_utc"]).astimezone(UTC),
            start_lcl=datetime.fromisoformat(simple_obj["start_lcl"]),
            start_hbt=datetime.fromisoformat(simple_obj["start_hbt"]),
            end_station=AirportCode(**simple_obj["end_station"]),
            end_utc=datetime.fromisoformat(simple_obj["end_utc"]).astimezone(UTC),
            end_lcl=datetime.fromisoformat(simple_obj["end_lcl"]),
            end_hbt=datetime.fromisoformat(simple_obj["end_hbt"]),
            flight_time=string_to_timedelta(simple_obj["flight_time"]),
            operating_time=string_to_timedelta(simple_obj["operating_time"]),
            soft_time=string_to_timedelta(simple_obj["soft_time"]),
            tafb=string_to_timedelta(simple_obj["tafb"]),
            dutyperiods=[DutyPeriod.from_simple(x) for x in simple_obj["dutyperiods"]],
        )
        return result

    def to_simple(self) -> TD.ExpandedTripTD:
        """Trip to simple object."""
        result = TD.ExpandedTripTD(
            source_uuid=self.source_uuid,
            source_idx=self.source_idx,
            uuid=self.uuid,
            trip_number=self.trip_number,
            base_equipment=self.base_equipment.to_simple(),
            positions=[TD.Position(name=x.name) for x in self.positions],
            operations=[TD.Operation(name=x.name) for x in self.operations],
            special_qual=self.special_qual,
            start_station=self.start_station.to_simple(),
            start_utc=self.start_utc.isoformat(),
            start_lcl=self.start_lcl.isoformat(),
            start_hbt=self.start_hbt.isoformat(),
            end_station=self.end_station.to_simple(),
            end_utc=self.end_utc.isoformat(),
            end_lcl=self.end_lcl.isoformat(),
            end_hbt=self.end_hbt.isoformat(),
            flight_time=timedelta_to_isoformat(self.flight_time),
            operating_time=timedelta_to_isoformat(self.operating_time),
            soft_time=timedelta_to_isoformat(self.soft_time),
            tafb=timedelta_to_isoformat(self.tafb),
            dutyperiods=[x.to_simple() for x in self.dutyperiods],
        )
        return result


def get_airport_code_from_iata(iata: str) -> AirportCode:
    """Get airport info from database."""
    airport = airport_from_iata(iata=iata)
    return AirportCode(
        iata=airport["iata"], icao=airport["icao"], tz_name=airport["tz"]
    )


# def default_file_name(trip: ExpandedTrip) -> str:
#     """Assemble a file name from trip data."""
#     ret_value: list[str] = []
#     ret_value.append(trip.start_lcl.date().isoformat())
#     ret_value.append(f"_{trip.base_equipment.base.iata}")
#     if trip.base_equipment.satellite_base:
#         ret_value.append(f"_{trip.base_equipment.satellite_base.iata}")
#     ret_value.append(f"_{trip.base_equipment.equipment}")
#     ret_value.append(f"_{trip.trip_number}.json")
#     return "".join(ret_value)


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
