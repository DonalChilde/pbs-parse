"""Structured model of a parsed trip, no translations from strings to more complex data."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Optional
from uuid import NAMESPACE_DNS, UUID, uuid5

from pfmsoft.simple_serializer import DataclassSerializer

from pbs_parse.pbs_2022_01.models import structured_TD as TD
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


@dataclass(slots=True)
class Transportation:
    """Transportatin."""

    name: str
    phone: str


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


@dataclass(slots=True)
class MonthDay:
    """MonthDay."""

    month: str
    day: str


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


@dataclass(slots=True)
class ExternalData:
    """ExternalData."""

    effective_from: str
    effective_to: str


@dataclass(slots=True)
class StructuredTrip:
    """StructuredTrip."""

    source: str
    page_idx: int
    trip_idx: int
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
    uuid: str = ""
    positions: list[str] = field(default_factory=list)
    operations: list[str] = field(default_factory=list)
    dutyperiods: list[DutyPeriod] = field(default_factory=list)
    calendar: list[str] = field(default_factory=list)

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
        """Make a uuid from a namespace and the source uuid string."""
        return uuid5(namespace=STRUCTURED_TRIP_NS, name=self.source)

    def default_file_name(self) -> str:
        """default_file_name.

        Returns:
            str: _description_
        """
        return f"structured-trip_page_{self.page_idx}_trip_{self.trip_idx}_{self.uuid}.json"

    @staticmethod
    def from_simple(simple_obj: TD.StructuredTripTD) -> "StructuredTrip":
        """from_simple.

        Args:
            simple_obj (TD.StructuredTripTD): _description_

        Returns:
            StructuredTrip: _description_
        """
        result = StructuredTrip(
            uuid=simple_obj["uuid"],
            source=simple_obj["source"],
            page_idx=simple_obj["page_idx"],
            trip_idx=simple_obj["trip_idx"],
            number=simple_obj["number"],
            ops_count=simple_obj["ops_count"],
            block=simple_obj["block"],
            synth=simple_obj["synth"],
            total_pay=simple_obj["total_pay"],
            tafb=simple_obj["tafb"],
            external=ExternalData(**simple_obj["external"]),
            page_header=PageHeader.from_simple(simple_obj=simple_obj["page_header"]),
            page_footer=PageFooter(**simple_obj["page_footer"]),
            positions=simple_obj["positions"],
            operations=simple_obj["operations"],
            special_qual=simple_obj["special_qual"],
            dutyperiods=[DutyPeriod.from_simple(x) for x in simple_obj["dutyperiods"]],
            calendar=simple_obj["calendar"],
        )
        return result


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
        complex_factory=StructuredTrip.from_simple
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
            glob (str, optional): The glob to match files. Defaults to "parsed_trip_*.json".
        """
        super().__init__(path_in, glob)

    def _translate(self, obj_path: Path) -> StructuredTrip:
        return STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=obj_path)
