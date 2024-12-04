"""Expected output from pyparsing grammar when converted to dict."""

from typing import TypedDict


class MonthDay(TypedDict):
    """The parts of a date, without the year."""

    month: str
    day: str


class PageHeader2(TypedDict):
    """The second line of a page, contains the from to date for the calendar."""

    from_date: MonthDay
    to_date: MonthDay


class BaseEquipment(TypedDict):
    """Matches the base equipment line/section.

    This data can be found on the base equipment line on the first page of each
    section, and also as part of the page footer.
    """

    base: str
    satellite_base: str
    equipment: str


class TripHeader(TypedDict):
    """Matches a trip header."""

    trip_number: str
    ops_count: str
    positions: list[str]
    operations: list[str]
    special_qual: bool
    prior_month_trip: bool


class DualTime(TypedDict):
    """Two times. Local and home base time."""

    lcl: str
    hbt: str


class DutyperiodReport(TypedDict):
    """The report time for a dutyperiod, and a list of calendar entries.

    The calendar entry list may be empty.
    """

    report: DualTime
    calendar_entries: list[str]


class Flight(TypedDict):
    """A flight."""

    dutyperiod_idx: str
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
    calendar_entries: list[str]


class DutyPeriodRelease(TypedDict):
    """A dutyperiod release."""

    release: DualTime
    block: str
    synth: str
    total_pay: str
    duty: str
    flight_duty: str
    calendar_entries: list[str]


class Layover(TypedDict):
    """A layover."""

    layover_city: str
    hotel_name: str
    hotel_phone: str
    rest: str
    calendar_entries: list[str]


class HotelAdditional(TypedDict):
    """An additional hotel."""

    layover_city: str
    name: str
    phone: str
    calendar_entries: list[str]


class Transportation(TypedDict):
    """transportation."""

    name: str
    phone: str
    calendar_entries: list[str]


class TripFooter(TypedDict):
    """The trip footer."""

    block: str
    synth: str
    total_pay: str
    tafb: str
    calendar_entries: list[str]


class CalendarOnly(TypedDict):
    """A line with only calendar entries."""

    calendar_entries: list[str]


class PageFooter(TypedDict):
    """The page footer."""

    issued: str
    effective: str
    base: str
    satellite_base: str
    equipment: str
    division: str
    page: str
