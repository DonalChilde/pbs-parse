"""Data model for a `Trip`."""

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from uuid import NAMESPACE_DNS, UUID, uuid5
from zoneinfo import ZoneInfo

from pfmsoft.simple_serializer import DataclassSerializer

import pbs_parse.pbs_2022_01.models.expanded_TD as TD
from pbs_parse.airports import airport_from_iata
from pbs_parse.snippets.datetime.iso8601_duration import (
    string_to_timedelta,
    timedelta_to_isoformat,
)

TRIP_NS = uuid5(NAMESPACE_DNS, "pbs_parse.pbs_2022_01.trip")


@dataclass(slots=True)
class Position:
    """A position, eg. CA or FO."""

    name: str


@dataclass(slots=True)
class AirportCode:
    """Airport/city identifiers."""

    iata: str
    icao: str
    tz_name: str

    def to_simple(self) -> TD.AirportCode:
        """AirportCode to simple."""
        result = TD.AirportCode(iata=self.iata, icao=self.icao, tz_name=self.tz_name)
        return result


@dataclass(slots=True)
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


@dataclass(slots=True)
class Operation:
    """An area of operation."""

    name: str


@dataclass(slots=True)
class Flight:
    """A flight."""

    eq_code: str
    number: str
    departure_station: AirportCode
    departure_utc: datetime
    arrival_station: AirportCode
    arrival_utc: datetime
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
            arrival_station=self.arrival_station.to_simple(),
            arrival_utc=self.arrival_utc.isoformat(),
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
            arrival_station=AirportCode(**simple_obj["arrival_station"]),
            arrival_utc=datetime.fromisoformat(simple_obj["arrival_utc"]).astimezone(
                UTC
            ),
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

    def depart_local(self) -> datetime:
        """Depart in local timezone."""
        return self.departure_utc.astimezone(ZoneInfo(self.departure_station.tz_name))

    def arrive_local(self) -> datetime:
        """Arrive in local timezone."""
        return self.arrival_utc.astimezone(ZoneInfo(self.arrival_station.tz_name))

    def depart(self, tz_name: str) -> datetime:
        """Depart in timezone."""
        return self.departure_utc.astimezone(ZoneInfo(tz_name))

    def arrive(self, tz_name: str) -> datetime:
        """Arrive in timezone."""
        return self.arrival_utc.astimezone(ZoneInfo(tz_name))


@dataclass(slots=True)
class Transportation:
    """Transpo."""

    name: str
    phone: str


@dataclass(slots=True)
class Hotel:
    """A Hotel."""

    name: str
    phone: str
    trans: list[Transportation]

    def to_simple(self) -> TD.Hotel:
        """Hotel to simple."""
        result = TD.Hotel(
            name=self.name,
            phone=self.phone,
            trans=[TD.Transportation(name=x.name, phone=x.phone) for x in self.trans],
        )
        return result

    @staticmethod
    def from_simple(simple_obj: TD.Hotel) -> "Hotel":
        """Hotel from simple."""
        result = Hotel(
            name=simple_obj["name"],
            phone=simple_obj["phone"],
            trans=[Transportation(**x) for x in simple_obj["trans"]],
        )
        return result


@dataclass(slots=True)
class Layover:
    """A Layover."""

    layover_station: AirportCode
    start_utc: datetime
    end_utc: datetime
    rest: timedelta
    hotels: list[Hotel] = field(default_factory=list)

    def to_simple(self) -> TD.Layover:
        """Layover to simple."""
        result = TD.Layover(
            layover_station=self.layover_station.to_simple(),
            start_utc=self.start_utc.isoformat(),
            end_utc=self.end_utc.isoformat(),
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
            end_utc=datetime.fromisoformat(simple_obj["end_utc"]).astimezone(UTC),
            hotels=[Hotel.from_simple(x) for x in simple_obj["hotels"]],
            rest=string_to_timedelta(simple_obj["rest"]),
        )
        return result

    def start_local(self) -> datetime:
        """Start in local timezone."""
        return self.start_utc.astimezone(ZoneInfo(self.layover_station.tz_name))

    def end_local(self) -> datetime:
        """End in local timezone."""
        return self.end_utc.astimezone(ZoneInfo(self.layover_station.tz_name))

    def start(self, tz_name: str) -> datetime:
        """Start in timezone."""
        return self.start_utc.astimezone(ZoneInfo(tz_name))

    def end(self, tz_name: str) -> datetime:
        """End in timezone."""
        return self.end_utc.astimezone(ZoneInfo(tz_name))


@dataclass(slots=True)
class DutyPeriod:
    """A dutyperiod."""

    report_station: AirportCode
    report_utc: datetime
    release_station: AirportCode
    release_utc: datetime
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
            release_station=self.release_station.to_simple(),
            release_utc=self.release_utc.isoformat(),
            flights=[x.to_simple() for x in self.flights],
            duty=timedelta_to_isoformat(self.duty),
            flight_duty=timedelta_to_isoformat(self.flight_duty),
            operating_time=timedelta_to_isoformat(self.operating_time),
            flight_time=timedelta_to_isoformat(self.operating_time),
            soft_time=timedelta_to_isoformat(self.soft_time),
            layover=layover,
        )
        return result

    def report_local(self) -> datetime:
        """Report in local timezone."""
        return self.report_utc.astimezone(ZoneInfo(self.report_station.tz_name))

    def release_local(self) -> datetime:
        """Release in local timezone."""
        return self.release_utc.astimezone(ZoneInfo(self.release_station.tz_name))

    def report(self, tz_name: str) -> datetime:
        """Report in timezone."""
        return self.report_utc.astimezone(ZoneInfo(tz_name))

    def release(self, tz_name: str) -> datetime:
        """Release in timezone."""
        return self.release_utc.astimezone(ZoneInfo(tz_name))

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
            release_station=AirportCode(**simple_obj["release_station"]),
            release_utc=datetime.fromisoformat(simple_obj["release_utc"]).astimezone(
                UTC
            ),
            flights=[Flight.from_simple(x) for x in simple_obj["flights"]],
            duty=string_to_timedelta(simple_obj["duty"]),
            flight_duty=string_to_timedelta(simple_obj["flight_duty"]),
            operating_time=string_to_timedelta(simple_obj["operating_time"]),
            flight_time=string_to_timedelta(simple_obj["flight_time"]),
            soft_time=string_to_timedelta(simple_obj["soft_time"]),
            layover=layover,
        )
        return result


@dataclass(slots=True)
class ExpandedTrip:
    """A trip."""

    source: str
    trip_number: str
    base_equipment: BaseEquipment
    special_qual: bool
    start_station: AirportCode
    start_utc: datetime
    end_station: AirportCode
    end_utc: datetime
    flight_time: timedelta
    operating_time: timedelta
    soft_time: timedelta
    tafb: timedelta
    uuid: str = ""
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
            name=f"{self.source}{self.start_utc.isoformat()}{self.trip_number}",
        )

    @staticmethod
    def from_simple(simple_obj: TD.ExpandedTrip) -> "ExpandedTrip":
        """Turn simple object into Trip."""
        result = ExpandedTrip(
            source=simple_obj["source"],
            trip_number=simple_obj["trip_number"],
            base_equipment=BaseEquipment.from_simple(simple_obj["base_equipment"]),
            positions=[Position(name=x["name"]) for x in simple_obj["positions"]],
            operations=[Operation(name=x["name"]) for x in simple_obj["operations"]],
            special_qual=simple_obj["special_qual"],
            start_station=AirportCode(**simple_obj["start_station"]),
            start_utc=datetime.fromisoformat(simple_obj["start_utc"]).astimezone(UTC),
            end_station=AirportCode(**simple_obj["end_station"]),
            end_utc=datetime.fromisoformat(simple_obj["end_utc"]).astimezone(UTC),
            flight_time=string_to_timedelta(simple_obj["flight_time"]),
            operating_time=string_to_timedelta(simple_obj["operating_time"]),
            soft_time=string_to_timedelta(simple_obj["soft_time"]),
            tafb=string_to_timedelta(simple_obj["tafb"]),
            dutyperiods=[DutyPeriod.from_simple(x) for x in simple_obj["dutyperiods"]],
        )
        return result

    def to_simple(self) -> TD.ExpandedTrip:
        """Trip to simple object."""
        result = TD.ExpandedTrip(
            source=self.source,
            trip_number=self.trip_number,
            base_equipment=self.base_equipment.to_simple(),
            positions=[TD.Position(name=x.name) for x in self.positions],
            operations=[TD.Operation(name=x.name) for x in self.operations],
            special_qual=self.special_qual,
            start_station=self.start_station.to_simple(),
            start_utc=self.start_utc.isoformat(),
            end_station=self.end_station.to_simple(),
            end_utc=self.end_utc.isoformat(),
            flight_time=timedelta_to_isoformat(self.flight_time),
            operating_time=timedelta_to_isoformat(self.operating_time),
            soft_time=timedelta_to_isoformat(self.soft_time),
            tafb=timedelta_to_isoformat(self.tafb),
            dutyperiods=[x.to_simple() for x in self.dutyperiods],
        )
        return result

    def start_local(self) -> datetime:
        """Start in local timezone."""
        return self.start_utc.astimezone(ZoneInfo(self.start_station.tz_name))

    def end_local(self) -> datetime:
        """End in local timezone."""
        return self.end_utc.astimezone(ZoneInfo(self.end_station.tz_name))

    def start(self, tz_name: str) -> datetime:
        """Start in timezone."""
        return self.start_utc.astimezone(ZoneInfo(tz_name))

    def end(self, tz_name: str) -> datetime:
        """End in timezone."""
        return self.end_utc.astimezone(ZoneInfo(tz_name))


def get_airport_code_from_iata(iata: str) -> AirportCode:
    """Get airport info from database."""
    airport = airport_from_iata(iata=iata)
    return AirportCode(
        iata=airport["iata"], icao=airport["icao"], tz_name=airport["tz"]
    )


def trip_serializer() -> DataclassSerializer[ExpandedTrip, TD.ExpandedTrip]:
    """Init a Trip serializer.

    Returns:
        DataclassSerializer[Trip, TD.Trip]: _description_
    """
    return DataclassSerializer[ExpandedTrip, TD.ExpandedTrip](
        complex_factory=ExpandedTrip.from_simple, simple_factory=ExpandedTrip.to_simple
    )


EXPANDED_TRIP_SERIALIZER = trip_serializer()


def default_file_name(trip: ExpandedTrip) -> str:
    """Assemble a file name from trip data."""
    ret_value: list[str] = []
    ret_value.append(trip.start_local().date().isoformat())
    ret_value.append(f"_{trip.base_equipment.base.iata}")
    if trip.base_equipment.satellite_base:
        ret_value.append(f"_{trip.base_equipment.satellite_base.iata}")
    ret_value.append(f"_{trip.base_equipment.equipment}")
    ret_value.append(f"_{trip.trip_number}.json")
    return "".join(ret_value)
