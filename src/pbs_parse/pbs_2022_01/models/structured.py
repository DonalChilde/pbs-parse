"""Structured model of a parsed trip, no translations from strings to more complex data."""

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Optional
from uuid import NAMESPACE_DNS, uuid5

from pfmsoft.simple_serializer import DataclassSerializer

from pbs_parse.pbs_2022_01.models import structured_TD as TD
from pbs_parse.pbs_2022_01.models.external_data import ExternalData
from pbs_parse.snippets.datetime.date_range import date_range
from pbs_parse.snippets.datetime.duration_regex import pattern_HHHMM
from pbs_parse.snippets.file.data_file_loader import DataFileLoader

STRUCTURED_TRIP_NS = uuid5(NAMESPACE_DNS, "pbs_parse.pbs_2022_01.structured_trip")
DURATION_REGEX = pattern_HHHMM(".")


@dataclass(slots=True)
class DualTime:
    """DualTime."""

    lcl: str
    hbt: str

    def to_simple(self) -> TD.DualTime:
        return TD.DualTime(lcl=self.lcl, hbt=self.hbt)


@dataclass(slots=True)
class Transportation:
    """Transportatin."""

    name: str
    phone: str

    def to_simple(self) -> TD.Transportation:
        return TD.Transportation(name=self.name, phone=self.phone)


@dataclass(slots=True)
class Hotel:
    """Hotel."""

    name: str
    phone: str
    transportation: list[Transportation] = field(default_factory=list)

    @staticmethod
    def from_simple(simple_obj: TD.Hotel) -> "Hotel":
        """from_simple.

        Args:
            simple_obj (TD.Hotel): _description_

        Returns:
            Hotel: _description_
        """
        result = Hotel(
            name=simple_obj["name"],
            phone=simple_obj["phone"],
            transportation=[Transportation(**x) for x in simple_obj["transportation"]],
        )

        return result

    def to_simple(self) -> TD.Hotel:
        return TD.Hotel(
            name=self.name,
            phone=self.phone,
            transportation=[x.to_simple() for x in self.transportation],
        )


@dataclass(slots=True)
class Layover:
    """Layover."""

    rest: str
    city: str
    hotels: list[Hotel] = field(default_factory=list)

    @staticmethod
    def from_simple(simple_obj: TD.Layover | None) -> Optional["Layover"]:
        """from_simple.

        Returns:
            TD.Layover | None: _description_
        """
        if simple_obj is None:
            return None
        result = Layover(
            rest=simple_obj["rest"],
            city=simple_obj["city"],
            hotels=[Hotel.from_simple(x) for x in simple_obj["hotels"]],
        )
        return result

    def to_simple(self) -> TD.Layover:
        """To simple."""
        return TD.Layover(
            rest=self.rest, city=self.city, hotels=[x.to_simple() for x in self.hotels]
        )


@dataclass(slots=True)
class Flight:
    """Flight."""

    dutyperiod_idx: str
    idx: str
    depart_day: str
    arrive_day: str
    equipment_code: str
    flight_number: str
    deadhead: bool
    deadhead_code: str
    departure_station: str
    departure_time: DualTime
    crew_meal: str
    arrival_station: str
    arrival_time: DualTime
    block: str
    synth: str
    ground: str
    equipment_change: bool

    @staticmethod
    def from_simple(simple_obj: TD.Flight) -> "Flight":
        """from_simple.

        Args:
            simple_obj (TD.Flight): _description_

        Returns:
            Flight: _description_
        """
        result = Flight(
            dutyperiod_idx=simple_obj["dutyperiod_idx"],
            idx=simple_obj["idx"],
            depart_day=simple_obj["depart_day"],
            arrive_day=simple_obj["arrive_day"],
            equipment_code=simple_obj["equipment_code"],
            flight_number=simple_obj["flight_number"],
            deadhead=simple_obj["deadhead"],
            deadhead_code=simple_obj["deadhead_code"],
            departure_station=simple_obj["departure_station"],
            departure_time=DualTime(**simple_obj["departure_time"]),
            crew_meal=simple_obj["crew_meal"],
            arrival_station=simple_obj["arrival_station"],
            arrival_time=DualTime(**simple_obj["arrival_time"]),
            block=simple_obj["block"],
            synth=simple_obj["synth"],
            ground=simple_obj["ground"],
            equipment_change=simple_obj["equipment_change"],
        )

        return result

    def to_simple(self) -> TD.Flight:
        """To simple."""
        return TD.Flight(
            dutyperiod_idx=self.dutyperiod_idx,
            idx=self.idx,
            depart_day=self.depart_day,
            arrive_day=self.arrive_day,
            equipment_code=self.equipment_code,
            flight_number=self.flight_number,
            deadhead=self.deadhead,
            deadhead_code=self.deadhead_code,
            departure_station=self.departure_station,
            departure_time=self.departure_time.to_simple(),
            crew_meal=self.crew_meal,
            arrival_station=self.arrival_station,
            arrival_time=self.arrival_time.to_simple(),
            block=self.block,
            synth=self.synth,
            ground=self.ground,
            equipment_change=self.equipment_change,
        )


@dataclass(slots=True)
class DutyPeriod:
    """DutyPeriod."""

    idx: str
    report_time: DualTime
    release_time: DualTime
    block: str
    synth: str
    total_pay: str
    duty: str
    flight_duty: str
    layover: Layover | None
    flights: list[Flight] = field(default_factory=list)

    @staticmethod
    def from_simple(simple_obj: TD.DutyPeriod) -> "DutyPeriod":
        """from_simple.

        Args:
            simple_obj (TD.DutyPeriod): _description_

        Returns:
            DutyPeriod: _description_
        """
        result = DutyPeriod(
            idx=simple_obj["idx"],
            report_time=DualTime(**simple_obj["report_time"]),
            release_time=DualTime(**simple_obj["release_time"]),
            block=simple_obj["block"],
            synth=simple_obj["synth"],
            total_pay=simple_obj["total_pay"],
            duty=simple_obj["duty"],
            flight_duty=simple_obj["flight_duty"],
            layover=Layover.from_simple(simple_obj["layover"]),
            flights=[Flight.from_simple(x) for x in simple_obj["flights"]],
        )
        return result

    def to_simple(self) -> TD.DutyPeriod:
        """To simple."""
        if self.layover is not None:
            layover = self.layover.to_simple()
        else:
            layover = None
        return TD.DutyPeriod(
            idx=self.idx,
            report_time=self.report_time.to_simple(),
            release_time=self.release_time.to_simple(),
            block=self.block,
            synth=self.synth,
            total_pay=self.total_pay,
            duty=self.duty,
            flight_duty=self.flight_duty,
            layover=layover,
            flights=[x.to_simple() for x in self.flights],
        )


@dataclass(slots=True)
class MonthDay:
    """MonthDay."""

    month: str
    day: str

    def to_simple(self) -> TD.MonthDay:
        """To simple."""
        return TD.MonthDay(month=self.month, day=self.day)


@dataclass(slots=True)
class PageHeader:
    """PageHeader."""

    from_date: MonthDay
    to_date: MonthDay

    @staticmethod
    def from_simple(simple_obj: TD.PageHeader) -> "PageHeader":
        """from_simple.

        Args:
            simple_obj (TD.PageHeader): _description_

        Returns:
            PageHeader: _description_
        """
        result = PageHeader(
            from_date=MonthDay(**simple_obj["from_date"]),
            to_date=MonthDay(**simple_obj["to_date"]),
        )
        return result

    def to_simple(self) -> TD.PageHeader:
        """To simple."""
        return TD.PageHeader(
            from_date=self.from_date.to_simple(), to_date=self.to_date.to_simple()
        )


@dataclass(slots=True)
class PageFooter:
    """PageFooter."""

    issued: str
    effective: str
    base: str
    satellite_base: str
    equipment: str
    division: str
    page: str

    def to_simple(self) -> TD.PageFooter:
        """To simple."""
        return TD.PageFooter(
            issued=self.issued,
            effective=self.effective,
            base=self.base,
            satellite_base=self.satellite_base,
            equipment=self.equipment,
            division=self.division,
            page=self.page,
        )


# @dataclass(slots=True)
# class ExternalData:
#     """ExternalData."""

#     effective_from: str
#     effective_to: str


@dataclass(slots=True)
class StructuredTripSource:
    """StructuredTripSource."""

    txt_file: str = "TXT_FILE"
    page_lines: str = "PAGE_LINES"
    trip_lines: str = "TRIP_LINES"
    parsed_trip: str = "PARSED_TRIP"

    def to_simple(self) -> TD.StructuredTripSourceTD:
        """To simple."""
        return TD.StructuredTripSourceTD(
            txt_file=self.txt_file,
            page_lines=self.page_lines,
            trip_lines=self.trip_lines,
            parsed_trip=self.parsed_trip,
        )

    @staticmethod
    def from_simple(value: TD.StructuredTripSourceTD):
        """From simple."""
        return StructuredTripSource(
            txt_file=value["txt_file"],
            page_lines=value["page_lines"],
            trip_lines=value["trip_lines"],
            parsed_trip=value["parsed_trip"],
        )


@dataclass(slots=True)
class StructuredTrip:
    """StructuredTrip."""

    source: StructuredTripSource
    idx: str
    number: str
    ops_count: str
    special_qual: bool
    block: str
    synth: str
    total_pay: str
    tafb: str
    external: ExternalData
    page_header: PageHeader
    page_footer: PageFooter
    positions: list[str] = field(default_factory=list)
    operations: list[str] = field(default_factory=list)
    dutyperiods: list[DutyPeriod] = field(default_factory=list)
    calendar: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def default_file_name(self) -> str:
        """default_file_name.

        Returns:
            str: _description_
        """
        return self.assemble_file_name(idx=self.idx, external=self.external)

    @staticmethod
    def assemble_file_name(idx: str, external: ExternalData) -> str:
        """assemble_file_name.

        Args:
            idx (str): _description_
            external (ExternalData): _description_

        Returns:
            str: _description_
        """
        return f"structured-trip_{external.base}_{external.effective_from}_{idx}.json"

    @staticmethod
    def from_simple(simple_obj: TD.StructuredTripTD) -> "StructuredTrip":
        """from_simple.

        Args:
            simple_obj (TD.StructuredTripTD): _description_

        Returns:
            StructuredTrip: _description_
        """
        result = StructuredTrip(
            source=StructuredTripSource.from_simple(simple_obj["source"]),
            # uuid=simple_obj["uuid"],
            # source_uuid=simple_obj["source_uuid"],
            idx=simple_obj["idx"],
            number=simple_obj["number"],
            ops_count=simple_obj["ops_count"],
            block=simple_obj["block"],
            synth=simple_obj["synth"],
            total_pay=simple_obj["total_pay"],
            tafb=simple_obj["tafb"],
            external=ExternalData.from_simple(simple_obj["external"]),
            page_header=PageHeader.from_simple(simple_obj=simple_obj["page_header"]),
            page_footer=PageFooter(**simple_obj["page_footer"]),
            positions=deepcopy(simple_obj["positions"]),
            operations=deepcopy(simple_obj["operations"]),
            special_qual=simple_obj["special_qual"],
            dutyperiods=[DutyPeriod.from_simple(x) for x in simple_obj["dutyperiods"]],
            calendar=deepcopy(simple_obj["calendar"]),
            errors=deepcopy(simple_obj["errors"]),
        )
        return result

    def to_simple(self) -> TD.StructuredTripTD:
        """To simple."""
        return TD.StructuredTripTD(
            source=self.source.to_simple(),
            # uuid=self.uuid,
            # source_uuid=self.source_uuid,
            idx=self.idx,
            number=self.number,
            ops_count=self.ops_count,
            block=self.block,
            synth=self.synth,
            total_pay=self.total_pay,
            tafb=self.tafb,
            external=self.external.to_simple(),
            page_header=self.page_header.to_simple(),
            page_footer=self.page_footer.to_simple(),
            positions=deepcopy(self.positions),
            operations=deepcopy(self.operations),
            special_qual=self.special_qual,
            dutyperiods=[x.to_simple() for x in self.dutyperiods],
            calendar=deepcopy(self.calendar),
            errors=deepcopy(self.errors),
        )


def build_start_dates(
    effective_from: date, effective_to: date, calendar: list[str]
) -> list[date]:
    """Gets the full date for a calendar entry.

    Raises:
        ValueError if full date cannot be found.
    """
    effective_dates = list(date_range(start_date=effective_from, end_date=effective_to))
    if len(effective_dates) != len(calendar):
        raise ValueError(
            f"The length of effective_dates {effective_dates!r} does not match the length of calendar {calendar!r}"
        )
    result: list[date] = []
    for idx, item in enumerate(calendar):
        if item.isnumeric():
            if effective_dates[idx].day != int(item):
                raise ValueError(
                    f"Calendar item {item} does not have the same day as {effective_dates[idx]}"
                )
            result.append(effective_dates[idx])
    return result


def parse_duration(duration_string: str) -> timedelta:
    """parse_duration.

    Args:
        duration_string (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        timedelta: _description_
    """
    match = DURATION_REGEX.fullmatch(duration_string)
    if match is None:
        raise ValueError(
            f"No match found for {duration_string} does it match the pattern HHH.MM?"
        )
    data = match.groupdict()
    hours = int(data["hours"])
    minutes = int(data["minutes"])
    return timedelta(hours=hours, minutes=minutes)


def structured_trip_serializer() -> (
    DataclassSerializer[StructuredTrip, TD.StructuredTripTD]
):
    """structured_trip_serializer.

    Returns:
        _type_: _description_
    """
    return DataclassSerializer[StructuredTrip, TD.StructuredTripTD](
        complex_factory=StructuredTrip.from_simple,
        simple_factory=StructuredTrip.to_simple,
    )


STRUCTURED_TRIP_SERIALIZER = structured_trip_serializer()


class StructuredTripSaver:
    """StructuredTripSaver."""

    def __init__(self, path_out: Path) -> None:
        """Save StructuredTrip to a directory using the default file name.

        Args:
            path_out (Path): The directory to save the StructuredTrip to.
        """
        if path_out.is_file():
            raise ValueError(
                f"Path out is an existing file, should be a directory. {path_out=}"
            )
        self.path_out = path_out

    def __call__(
        self, structured_trip: StructuredTrip, overwrite: bool = False
    ) -> Path:
        """Save StructuredTrip to a directory using the default file name.

        Args:
            structured_trip (StructuredTrip): The StructuredTrip to save.
            overwrite (bool): Overwrite existing files.

        Returns:
            Path: The path to the saved file.
        """
        path_out = self.path_out / structured_trip.default_file_name()
        STRUCTURED_TRIP_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=structured_trip, overwrite=overwrite
        )
        return path_out


class StructuredTripLoader(DataFileLoader[StructuredTrip]):
    """StructuredTripLoader."""

    def __init__(self, path_in: Path, glob: str = "structured-trip_*.json") -> None:
        """Load StructuredTrip from directory.

        Args:
            path_in (Path): The directory to load files from.
            glob (str, optional): The glob to match files. Defaults to "structured-trip_*.json".
        """
        super().__init__(path_in, glob)

    def _translate(self, obj_path: Path) -> StructuredTrip:
        return STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=obj_path)
