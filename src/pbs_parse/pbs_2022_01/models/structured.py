"""Structured model of a parsed trip, no translations from strings to more complex data."""

# ruff: noqa: D101 D102 D103
from dataclasses import dataclass, field
from typing import Optional
from uuid import NAMESPACE_DNS, UUID, uuid4, uuid5

from pfmsoft.simple_serializer import DataclassSerializer

from pbs_parse.pbs_2022_01.models import structured_TD as TD

STRUCTURED_TRIP_NS = uuid5(NAMESPACE_DNS, "pbs_parse.pbs_2022_01.structured_trip")


@dataclass(slots=True)
class Transportation:
    name: str
    phone: str


@dataclass(slots=True)
class Hotel:
    name: str
    phone: str
    transportation: list[Transportation] = field(default_factory=list)

    @staticmethod
    def from_simple(simple_obj: TD.Hotel) -> "Hotel":
        result = Hotel(
            name=simple_obj["name"],
            phone=simple_obj["phone"],
            transportation=[Transportation(**x) for x in simple_obj["transportation"]],
        )

        return result


@dataclass(slots=True)
class Layover:
    uuid: str
    rest: str
    city: str
    hotels: list[Hotel] = field(default_factory=list)

    @staticmethod
    def from_simple(simple_obj: TD.Layover | None) -> Optional["Layover"]:
        if simple_obj is None:
            return None
        result = Layover(
            uuid=simple_obj["uuid"],
            rest=simple_obj["rest"],
            city=simple_obj["city"],
            hotels=[Hotel.from_simple(x) for x in simple_obj["hotels"]],
        )
        return result


@dataclass(slots=True)
class Flight:
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


@dataclass(slots=True)
class DutyPeriod:
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
    flights: list[Flight] = field(default_factory=list)

    @staticmethod
    def from_simple(simple_obj: TD.DutyPeriod) -> "DutyPeriod":
        result = DutyPeriod(
            uuid=simple_obj["uuid"],
            idx=simple_obj["idx"],
            report_time=simple_obj["report_time"],
            release_time=simple_obj["release_time"],
            block=simple_obj["block"],
            synth=simple_obj["synth"],
            total_pay=simple_obj["total_pay"],
            duty=simple_obj["duty"],
            flight_duty=simple_obj["flight_duty"],
            layover=Layover.from_simple(simple_obj["layover"]),
            flights=[Flight(**x) for x in simple_obj["flights"]],
        )
        return result


@dataclass(slots=True)
class PageHeader:
    from_date: str
    to_date: str


@dataclass(slots=True)
class PageFooter:
    issued: str
    effective: str
    base: str
    satellite_base: str
    equipment: str
    division: str
    page: str


@dataclass(slots=True)
class ExternalData:
    effective_from: str
    effective_to: str


@dataclass(slots=True)
class StructuredTrip:
    source: str
    number: str
    ops_count: str
    block: str
    synth: str
    total_pay: str
    tafb: str
    external: ExternalData
    page_header: PageHeader
    page_footer: PageFooter
    uuid: str = ""
    positions: list[str] = field(default_factory=list)
    operations: list[str] = field(default_factory=list)
    qualifications: list[str] = field(default_factory=list)
    dutyperiods: list[DutyPeriod] = field(default_factory=list)
    calendar: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Init the uuid if missing, validate if not missing."""
        current_uuid_str = str(self.make_uuid())
        if self.uuid == "":
            self.uuid = current_uuid_str
            return
        # if self.uuid != current_uuid_str:
        #     raise ValueError(
        #         f"Supplied uuid: {self.uuid} does not match calculated uuid: {current_uuid_str}"
        #     )

    def make_uuid(self) -> UUID:
        """Make a uuid from a namespace and the repr of asdict(self), minus the uuid field."""
        # data = asdict(self)
        # data.pop("uuid", None)
        # return uuid5(STRUCTURED_TRIP_NS, repr(data))
        return uuid4()

    @staticmethod
    def from_simple(simple_obj: TD.StructuredTripTD) -> "StructuredTrip":
        result = StructuredTrip(
            uuid=simple_obj["uuid"],
            source=simple_obj["source"],
            number=simple_obj["number"],
            ops_count=simple_obj["ops_count"],
            block=simple_obj["block"],
            synth=simple_obj["synth"],
            total_pay=simple_obj["total_pay"],
            tafb=simple_obj["total_pay"],
            external=ExternalData(**simple_obj["external"]),
            page_header=PageHeader(**simple_obj["page_header"]),
            page_footer=PageFooter(**simple_obj["page_footer"]),
            positions=simple_obj["positions"],
            operations=simple_obj["operations"],
            qualifications=simple_obj["qualifications"],
            dutyperiods=[DutyPeriod.from_simple(x) for x in simple_obj["dutyperiods"]],
            calendar=simple_obj["calendar"],
        )
        return result


def structured_trip_serializer() -> (
    DataclassSerializer[StructuredTrip, TD.StructuredTripTD]
):
    return DataclassSerializer[StructuredTrip, TD.StructuredTripTD](
        complex_factory=StructuredTrip.from_simple
    )


def default_file_name(path_name: str) -> str:
    new_name = path_name.removesuffix(".parsed.json")
    return f"{new_name}.structured.json"
