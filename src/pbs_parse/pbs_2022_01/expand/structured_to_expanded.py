"""Translate a pbs_2022_01 format trip."""

import logging
from collections.abc import Sequence
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pbs_parse.pbs_2022_01.models.structured as ST
from pbs_parse.pbs_2022_01.models import expanded as model

logger = logging.getLogger(__name__)


def translate_structured_trip_from_file(path_in: Path) -> list[model.ExpandedTrip]:
    """Load a pbs_2022_01 structured trip from file and translate it to Trip."""
    s_trip = ST.structured_trip_serializer().load_from_json(path_in=path_in)
    return translate_structured_trip(s_trip=s_trip)


def translate_structured_trip(s_trip: ST.StructuredTrip) -> list[model.ExpandedTrip]:
    """Translate a pbs_2022_01 structured trip to Trip."""
    return _translate_trips(s_trip=s_trip)


def _translate_flight(
    departure_utc: datetime,
    departure_station: model.AirportCode,
    hbt_tz_name: str,
    s_flight: ST.Flight,
) -> model.Flight:
    zero = timedelta(seconds=0)
    arrival_station = model.get_airport_code_from_iata(iata=s_flight.arrival_station)
    operating_time = ST.parse_duration(s_flight.block)
    soft_time = ST.parse_duration(s_flight.synth)
    if operating_time > zero and soft_time == zero:
        arrival_utc = delta_dt(
            utc_ref=departure_utc,
            td=operating_time,
            lcl_ref=s_flight.arrival_time.lcl,
            lcl_tz=arrival_station.tz_name,
        )
    elif operating_time == zero and soft_time > zero:
        arrival_utc = delta_dt(
            utc_ref=departure_utc,
            td=soft_time,
            lcl_ref=s_flight.arrival_time.lcl,
            lcl_tz=arrival_station.tz_name,
        )
    else:
        raise ValueError(
            f"Inconsistent soft and operating times for structured flight. {s_flight}"
        )
    flight_time = arrival_utc - departure_utc

    try:
        ground_time = ST.parse_duration(s_flight.ground)
    except ValueError:
        ground_time = timedelta(hours=0)

    return model.Flight(
        eq_code=s_flight.equipment_code,
        number=s_flight.flight_number,
        departure_station=departure_station,
        departure_utc=departure_utc,
        departure_lcl=departure_utc.astimezone(ZoneInfo(departure_station.tz_name)),
        departure_hbt=departure_utc.astimezone(ZoneInfo(hbt_tz_name)),
        arrival_station=arrival_station,
        arrival_utc=arrival_utc,
        arrival_lcl=arrival_utc.astimezone(ZoneInfo(arrival_station.tz_name)),
        arrival_hbt=arrival_utc.astimezone(ZoneInfo(hbt_tz_name)),
        deadhead=bool(s_flight.deadhead),
        deadhead_code=s_flight.deadhead_code,
        crewmeal=s_flight.crew_meal,
        eq_change=bool(s_flight.equipment_change),
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        ground_time=ground_time,
    )


def _translate_flights(
    first_departure_utc: datetime,
    s_flights: Sequence[ST.Flight],
    hbt_tz_name: str,
) -> list[model.Flight]:
    flights: list[model.Flight] = []
    departure_utc = first_departure_utc
    for s_flight in s_flights:
        departure_station = model.get_airport_code_from_iata(s_flight.departure_station)
        flight = _translate_flight(
            departure_utc=departure_utc,
            departure_station=departure_station,
            hbt_tz_name=hbt_tz_name,
            s_flight=s_flight,
        )
        departure_utc = flight.arrival_utc + flight.ground_time
        flights.append(flight)
    return flights


def _translate_dutyperiod(
    report_utc: datetime,
    hbt_tz_name: str,
    next_report_lcl: str,
    s_dutyperiod: ST.DutyPeriod,
) -> model.DutyPeriod:
    report_station = model.get_airport_code_from_iata(
        iata=s_dutyperiod.flights[0].departure_station
    )
    release_station = model.get_airport_code_from_iata(
        s_dutyperiod.flights[-1].arrival_station
    )
    duty = ST.parse_duration(s_dutyperiod.duty)
    release_utc = delta_dt(
        utc_ref=report_utc,
        td=duty,
        lcl_ref=s_dutyperiod.release_time.lcl,
        lcl_tz=release_station.tz_name,
    )
    flight_duty = ST.parse_duration(s_dutyperiod.flight_duty)
    operating_time = ST.parse_duration(s_dutyperiod.block)
    soft_time = ST.parse_duration(s_dutyperiod.synth)
    first_departure_delta = report_to_first_flight_delta(s_dutyperiod=s_dutyperiod)
    first_departure_utc = delta_dt(
        utc_ref=report_utc,
        td=first_departure_delta,
        lcl_ref=s_dutyperiod.flights[0].departure_time.lcl,
        lcl_tz=report_station.tz_name,
    )
    flights = _translate_flights(
        first_departure_utc=first_departure_utc,
        hbt_tz_name=hbt_tz_name,
        s_flights=s_dutyperiod.flights,
    )
    layover = _translate_layover(
        dutyperiod_release_utc=release_utc,
        hbt_tz_name=hbt_tz_name,
        next_report_lcl=next_report_lcl,
        s_layover=s_dutyperiod.layover,
    )
    flight_time = timedelta(
        seconds=sum([x.flight_time.total_seconds() for x in flights])
    )
    return model.DutyPeriod(
        report_station=report_station,
        report_utc=report_utc,
        report_lcl=report_utc.astimezone(ZoneInfo(report_station.tz_name)),
        report_hbt=report_utc.astimezone(ZoneInfo(hbt_tz_name)),
        release_station=release_station,
        release_utc=release_utc,
        release_lcl=release_utc.astimezone(ZoneInfo(release_station.tz_name)),
        release_hbt=release_utc.astimezone(ZoneInfo(hbt_tz_name)),
        flights=flights,
        duty=duty,
        flight_duty=flight_duty,
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        layover=layover,
    )


def _translate_dutyperiods(
    first_report_utc: datetime,
    hbt_tz_name: str,
    s_dutyperiods: Sequence[ST.DutyPeriod],
) -> list[model.DutyPeriod]:
    dutyperiods: list[model.DutyPeriod] = []
    report_utc = first_report_utc
    for idx, s_dutyperiod in enumerate(s_dutyperiods):
        try:
            next_report_lcl = s_dutyperiods[idx + 1].report_time.lcl
        except IndexError:
            next_report_lcl = ""
        dutyperiod = _translate_dutyperiod(
            report_utc=report_utc,
            hbt_tz_name=hbt_tz_name,
            next_report_lcl=next_report_lcl,
            s_dutyperiod=s_dutyperiod,
        )
        dutyperiods.append(dutyperiod)
        if dutyperiod.layover is not None:
            report_utc = dutyperiod.release_utc + dutyperiod.layover.rest
    return dutyperiods


def _translate_layover(
    dutyperiod_release_utc: datetime,
    hbt_tz_name: str,
    next_report_lcl: str,
    s_layover: ST.Layover | None,
) -> model.Layover | None:
    if s_layover is None:
        return None
    hotels = _translate_hotels(s_hotels=s_layover.hotels)
    layover_station = model.get_airport_code_from_iata(iata=s_layover.city)

    rest = ST.parse_duration(s_layover.rest)
    end_utc = delta_dt(
        utc_ref=dutyperiod_release_utc,
        td=rest,
        lcl_ref=next_report_lcl,
        lcl_tz=layover_station.tz_name,
    )
    return model.Layover(
        layover_station=layover_station,
        start_utc=dutyperiod_release_utc,
        start_lcl=dutyperiod_release_utc.astimezone(ZoneInfo(layover_station.tz_name)),
        start_hbt=dutyperiod_release_utc.astimezone(ZoneInfo(hbt_tz_name)),
        end_utc=end_utc,
        end_lcl=end_utc.astimezone(ZoneInfo(layover_station.tz_name)),
        end_hbt=end_utc.astimezone(ZoneInfo(hbt_tz_name)),
        rest=rest,
        hotels=hotels,
    )


def _translate_hotel(s_hotel: ST.Hotel) -> model.Hotel:
    transportation: list[model.Transportation] = []
    for s_trans in s_hotel.transportation:
        trans = model.Transportation(name=s_trans.name, phone=s_trans.phone)
        transportation.append(trans)
    hotel = model.Hotel(
        name=s_hotel.name, phone=s_hotel.phone, transportation=transportation
    )
    return hotel


def _translate_hotels(s_hotels: Sequence[ST.Hotel]) -> list[model.Hotel]:
    hotels: list[model.Hotel] = []
    for s_hotel in s_hotels:
        hotels.append(_translate_hotel(s_hotel=s_hotel))
    return hotels


def _transate_trip(s_trip: ST.StructuredTrip, start_date: date) -> model.ExpandedTrip:
    """Translate a StructuredTrip that starts on a particular date."""
    base_airport = model.get_airport_code_from_iata(s_trip.page_footer.base)
    first_report = time.fromisoformat(s_trip.dutyperiods[0].report_time.lcl)
    # Should be unambiguous unless start time is in the fold, Nov. dst switch 2am sunday.
    report_utc = datetime.combine(
        start_date, first_report, ZoneInfo(base_airport.tz_name)
    ).astimezone(UTC)
    dutyperiods = _translate_dutyperiods(
        first_report_utc=report_utc,
        hbt_tz_name=base_airport.tz_name,
        s_dutyperiods=s_trip.dutyperiods,
    )
    positions = [model.Position(name=x) for x in s_trip.positions]
    operations = [model.Operation(name=x) for x in s_trip.operations]
    flight_time = timedelta(
        seconds=sum([x.flight_time.total_seconds() for x in dutyperiods])
    )
    operating_time = ST.parse_duration(s_trip.block)
    soft_time = ST.parse_duration(s_trip.synth)
    tafb = ST.parse_duration(s_trip.tafb)
    try:
        satellite_base = model.get_airport_code_from_iata(
            iata=s_trip.page_footer.satellite_base
        )
    except ValueError:
        satellite_base = None
    base_equipment = model.BaseEquipment(
        base=base_airport,
        satellite_base=satellite_base,
        equipment=s_trip.page_footer.equipment,
    )
    return model.ExpandedTrip(
        source=s_trip.uuid,
        trip_number=s_trip.number,
        base_equipment=base_equipment,
        positions=positions,
        operations=operations,
        special_qual=s_trip.special_qual,
        start_station=dutyperiods[0].report_station,
        start_utc=dutyperiods[0].report_utc,
        start_lcl=dutyperiods[0].report_lcl,
        start_hbt=dutyperiods[0].report_hbt,
        end_station=dutyperiods[-1].release_station,
        end_utc=dutyperiods[-1].release_utc,
        end_lcl=dutyperiods[-1].release_lcl,
        end_hbt=dutyperiods[-1].release_hbt,
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        tafb=tafb,
        dutyperiods=dutyperiods,
    )


def _translate_trips(s_trip: ST.StructuredTrip) -> list[model.ExpandedTrip]:
    start_dates = ST.build_start_dates(
        effective_from=date.fromisoformat(s_trip.external.effective_from),
        effective_to=date.fromisoformat(s_trip.external.effective_to),
        calendar=s_trip.calendar,
    )
    trips: list[model.ExpandedTrip] = []
    for start_date in start_dates:
        trip = _transate_trip(s_trip=s_trip, start_date=start_date)
        trips.append(trip)
    return trips


def assemble_datetime(date_obj: date, time_str: str, tz_name: str) -> datetime:
    """Get the utc datetime for the first report of a trip.

    _extended_summary_

    Args:
        date_obj (date): _description_
        time_str (str): _description_
        tz_name (str): _description_

    Returns:
        datetime: The start of the trip in UTC.
    """
    tz_info = ZoneInfo(tz_name)
    time_local = time.fromisoformat(time_str)
    datetime_local = datetime.combine(date=date_obj, time=time_local, tzinfo=tz_info)
    datetime_utc = datetime_local.astimezone(UTC)
    return datetime_utc


def calculate_arrival(
    departure_utc: datetime,
    arrival_station: model.AirportCode,
    arrival_time_str: str,
) -> datetime:
    """Derive the utc arrival time, and use to build DatetimeTriple."""
    arrival_utc = next_local_time_in_utc(
        utc_start=departure_utc,
        next_lcl=time.fromisoformat(arrival_time_str),
        next_tz_name=arrival_station.tz_name,
    )
    return arrival_utc


def next_local_time_in_utc(
    utc_start: datetime, next_lcl: time, next_tz_name: str
) -> datetime:
    """Calculate the next occurance of a time in UTC.

    Calulate the next occurance of a datetime in UTC when only the
    following information is know.

    This does not handle times `in the fold` of DST. eg november fall back.

    Args:
        utc_start (datetime): The datetime in UTC to reference
        next_lcl (time): The local `time` that falls after `utc_start`
        next_tz_name (str): The timezone name of `next_nieve`.

    Returns:
        datetime: The next datetime in UTC
    """
    offset_tz = ZoneInfo(next_tz_name)
    next_datetime = datetime.combine(
        date=utc_start.astimezone(offset_tz).date(),
        time=next_lcl,
        tzinfo=offset_tz,
    )
    if next_datetime < utc_start.astimezone(offset_tz):
        # increment utc_start if `next_datetime` comes before a localized utc_start.
        utc_start = utc_start + timedelta(days=1)
        next_datetime = datetime.combine(
            date=utc_start.astimezone(offset_tz).date(),
            time=next_lcl,
            tzinfo=offset_tz,
        )
    return next_datetime.astimezone(UTC)


def report_to_first_flight_delta(s_dutyperiod: ST.DutyPeriod) -> timedelta:
    """Get the delta between report and the first flight.

    report to first departure should be 1 hour or 30 min for dh leg.
    """
    if s_dutyperiod.flights[0].deadhead:
        td_delta = timedelta(minutes=30)
    else:
        td_delta = timedelta(hours=1)
    return td_delta


def delta_dt(utc_ref: datetime, td: timedelta, lcl_ref: str, lcl_tz: str) -> datetime:
    """Get next utc time from uncertain info.

    Pbs pairing packages have some incorrect info sometimes.
    - during the nov. fold, a layover rest duration was an hour short when compared to release/report.

    figure out whether to use td addition, or next time calc to get accurate next utc.

    Args:
        utc_ref (datetime): _description_
        td (timedelta): _description_
        lcl_ref (str): _description_
        lcl_tz (str): _description_

    Returns:
        datetime: _description_
    """
    dt_utc = utc_ref + td
    dt_lcl = dt_utc.astimezone(ZoneInfo(lcl_tz))
    if dt_lcl.strftime("%H%M") != lcl_ref:
        logger.warning("%r time does not match %s. %r", dt_lcl, lcl_ref, locals())
        dt_alt = next_local_time_in_utc(
            utc_start=utc_ref, next_lcl=time.fromisoformat(lcl_ref), next_tz_name=lcl_tz
        )
        return dt_alt
    return dt_utc
