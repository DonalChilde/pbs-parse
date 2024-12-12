"""Data model for a `Trip`."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

import pbs_parse.pbs_2022_01.models.trip_TD as TD
from pbs_parse.airports import airport_from_iata
from pbs_parse.snippets.datetime.parse_iso8601_duration import parse_iso8601_duration
from pbs_parse.snippets.datetime.timedelta_to_iso8601 import timedelta_to_iso8601


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
    depart_utc: datetime
    arrival_station: AirportCode
    arrive_utc: datetime
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
            depart_utc=self.depart_utc.isoformat(),
            arrival_station=self.arrival_station.to_simple(),
            arrive_utc=self.arrive_utc.isoformat(),
            deadhead=self.deadhead,
            deadhead_code=self.deadhead_code,
            crewmeal=self.crewmeal,
            eq_change=self.eq_change,
            flight_time=timedelta_to_iso8601(self.flight_time),
            operating_time=timedelta_to_iso8601(self.operating_time),
            soft_time=timedelta_to_iso8601(self.soft_time),
            ground_time=timedelta_to_iso8601(self.ground_time),
        )

        return result

    @staticmethod
    def from_simple(simple_obj: TD.Flight) -> "Flight":
        """Flight from simple."""
        result = Flight(
            eq_code=simple_obj["eq_code"],
            number=simple_obj["number"],
            departure_station=AirportCode(**simple_obj["departure_station"]),
            depart_utc=datetime.fromisoformat(simple_obj["depart_utc"]).astimezone(UTC),
            arrival_station=AirportCode(**simple_obj["arrival_station"]),
            arrive_utc=datetime.fromisoformat(simple_obj["arrive_utc"]).astimezone(UTC),
            deadhead=simple_obj["deadhead"],
            deadhead_code=simple_obj["deadhead_code"],
            crewmeal=simple_obj["crewmeal"],
            eq_change=simple_obj["eq_change"],
            flight_time=parse_iso8601_duration(simple_obj["flight_time"]),
            operating_time=parse_iso8601_duration(simple_obj["operating_time"]),
            soft_time=parse_iso8601_duration(simple_obj["soft_time"]),
            ground_time=parse_iso8601_duration(simple_obj["ground_time"]),
        )
        return result

    def depart_local(self) -> datetime:
        """Depart in local timezone."""
        return self.depart_utc.astimezone(ZoneInfo(self.departure_station.tz_name))

    def arrive_local(self) -> datetime:
        """Arrive in local timezone."""
        return self.arrive_utc.astimezone(ZoneInfo(self.arrival_station.tz_name))

    def depart(self, tz_name: str) -> datetime:
        """Depart in timezone."""
        return self.depart_utc.astimezone(ZoneInfo(tz_name))

    def arrive(self, tz_name: str) -> datetime:
        """Arrive in timezone."""
        return self.arrive_utc.astimezone(ZoneInfo(tz_name))


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
    hotels: list[Hotel]
    rest: timedelta

    def to_simple(self) -> TD.Layover:
        """Layover to simple."""
        result = TD.Layover(
            layover_station=self.layover_station.to_simple(),
            start_utc=self.start_utc.isoformat(),
            end_utc=self.end_utc.isoformat(),
            hotels=[x.to_simple() for x in self.hotels],
            rest=timedelta_to_iso8601(self.rest),
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
            rest=parse_iso8601_duration(simple_obj["rest"]),
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
    flights: list[Flight]
    duty: timedelta
    flight_duty: timedelta
    operating_time: timedelta
    flight_time: timedelta
    soft_time: timedelta
    layover: Layover | None

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
            duty=timedelta_to_iso8601(self.duty),
            flight_duty=timedelta_to_iso8601(self.flight_duty),
            operating_time=timedelta_to_iso8601(self.operating_time),
            flight_time=timedelta_to_iso8601(self.operating_time),
            soft_time=timedelta_to_iso8601(self.soft_time),
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
            duty=parse_iso8601_duration(simple_obj["duty"]),
            flight_duty=parse_iso8601_duration(simple_obj["flight_duty"]),
            operating_time=parse_iso8601_duration(simple_obj["operating_time"]),
            flight_time=parse_iso8601_duration(simple_obj["flight_time"]),
            soft_time=parse_iso8601_duration(simple_obj["soft_time"]),
            layover=layover,
        )
        return result


@dataclass(slots=True)
class Trip:
    """A trip."""

    source: str
    trip_number: str
    base_equipment: BaseEquipment
    positions: list[Position]
    operations: list[Operation]
    special_qual: bool
    start_station: AirportCode
    start_utc: datetime
    end_station: AirportCode
    end_utc: datetime
    flight_time: timedelta
    operating_time: timedelta
    soft_time: timedelta
    tafb: timedelta
    dutyperiods: list[DutyPeriod]

    @staticmethod
    def from_simple(simple_obj: TD.Trip) -> "Trip":
        """Turn simple object into Trip."""
        result = Trip(
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
            flight_time=parse_iso8601_duration(simple_obj["flight_time"]),
            operating_time=parse_iso8601_duration(simple_obj["operating_time"]),
            soft_time=parse_iso8601_duration(simple_obj["soft_time"]),
            tafb=parse_iso8601_duration(simple_obj["tafb"]),
            dutyperiods=[DutyPeriod.from_simple(x) for x in simple_obj["dutyperiods"]],
        )
        return result

    def to_simple(self) -> TD.Trip:
        """Trip to simple object."""
        result = TD.Trip(
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
            flight_time=timedelta_to_iso8601(self.flight_time),
            operating_time=timedelta_to_iso8601(self.operating_time),
            soft_time=timedelta_to_iso8601(self.soft_time),
            tafb=timedelta_to_iso8601(self.tafb),
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
