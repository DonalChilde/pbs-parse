"""Translate structured to expanded."""

import logging
from collections.abc import Callable, Iterable, Iterator, Sequence
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Self
from zoneinfo import ZoneInfo

import pbs_parse.pbs_2022_01.models.structured as ST
from pbs_parse.pbs_2022_01.expand.state import State
from pbs_parse.pbs_2022_01.expand.translate_trips import translate_trips
from pbs_parse.pbs_2022_01.models import expanded as model
from pbs_parse.snippets.datetime.next_local_time import next_local_time

from .utc_to_local import utc_to_local

logger = logging.getLogger(__name__)
UTC = ZoneInfo("UTC")


class StructuredToExpanded:
    """StructuredToExpanded."""

    def __init__(self, structured_trip: ST.StructuredTrip) -> None:
        """__init__.

        Args:
            structured_trip (ST.StructuredTrip): _description_
        """
        self.s_trip = structured_trip
        self.base = model.get_airport_code_from_iata(self.s_trip.page_footer.base)
        self.hbt_tzinfo = ZoneInfo(self.base.tz_name)
        self.dp_idx = 0
        self.flight_idx = 0

    @classmethod
    def from_file(cls, path_in: Path) -> Self:
        """from_file.

        Args:
            path_in (Path): _description_

        Returns:
            StructuredToExpanded: _description_
        """
        return cls(
            structured_trip=ST.STRUCTURED_TRIP_SERIALIZER.load_from_json(
                path_in=path_in
            )
        )

    def translate(self) -> list[model.ExpandedTrip]:
        """Translate a pbs_2022_01 structured trip to Trip."""
        state = State(base=self.base, hbt_tzinfo=self.hbt_tzinfo)
        e_trips, state = translate_trips(s_trip=self.s_trip, state=state)
        return e_trips

    # def _translate_flight(
    #     self,
    #     departure_utc: datetime,
    #     departure_station: model.AirportCode,
    #     s_flight: ST.Flight,
    # ) -> model.Flight:
    #     zero = timedelta(seconds=0)
    #     arrival_station = model.get_airport_code_from_iata(
    #         iata=s_flight.arrival_station
    #     )
    #     operating_time = ST.parse_duration(s_flight.block)
    #     soft_time = ST.parse_duration(s_flight.synth)
    #     if operating_time > zero and soft_time == zero:
    #         arrival_utc = self._delta_dt(
    #             utc_ref=departure_utc,
    #             td=operating_time,
    #             lcl_ref=s_flight.arrival_time.lcl,
    #             lcl_tz=arrival_station.tz_name,
    #             field_name="arrival operating time",
    #         )
    #     elif operating_time == zero and soft_time > zero:
    #         arrival_utc = self._delta_dt(
    #             utc_ref=departure_utc,
    #             td=soft_time,
    #             lcl_ref=s_flight.arrival_time.lcl,
    #             lcl_tz=arrival_station.tz_name,
    #             field_name="arrival soft time",
    #         )
    #     else:
    #         raise ValueError(
    #             f"Inconsistent soft and operating times for structured flight. {s_flight}"
    #         )
    #     flight_time = arrival_utc - departure_utc

    #     try:
    #         ground_time = ST.parse_duration(s_flight.ground)
    #     except ValueError:
    #         ground_time = timedelta(hours=0)

    #     return model.Flight(
    #         eq_code=s_flight.equipment_code,
    #         number=s_flight.flight_number,
    #         departure_station=departure_station,
    #         departure_utc=departure_utc,
    #         departure_lcl=departure_utc.astimezone(ZoneInfo(departure_station.tz_name)),
    #         departure_hbt=departure_utc.astimezone(self.hbt_tzinfo),
    #         arrival_station=arrival_station,
    #         arrival_utc=arrival_utc,
    #         arrival_lcl=arrival_utc.astimezone(ZoneInfo(arrival_station.tz_name)),
    #         arrival_hbt=arrival_utc.astimezone(self.hbt_tzinfo),
    #         deadhead=bool(s_flight.deadhead),
    #         deadhead_code=s_flight.deadhead_code,
    #         crewmeal=s_flight.crew_meal,
    #         eq_change=bool(s_flight.equipment_change),
    #         flight_time=flight_time,
    #         operating_time=operating_time,
    #         soft_time=soft_time,
    #         ground_time=ground_time,
    #     )

    # def _translate_flights(
    #     self,
    #     first_departure_utc: datetime,
    #     s_flights: Sequence[ST.Flight],
    # ) -> list[model.Flight]:
    #     flights: list[model.Flight] = []
    #     departure_utc = first_departure_utc
    #     for idx, s_flight in enumerate(s_flights):
    #         self.flight_idx = idx + 1
    #         logger.debug(
    #             "Translating flight %d with departure_utc %s",
    #             self.flight_idx,
    #             departure_utc.isoformat(),
    #         )
    #         departure_station = model.get_airport_code_from_iata(
    #             s_flight.departure_station
    #         )
    #         flight = self._translate_flight(
    #             departure_utc=departure_utc,
    #             departure_station=departure_station,
    #             s_flight=s_flight,
    #         )
    #         departure_utc = flight.arrival_utc + flight.ground_time
    #         flights.append(flight)
    #     return flights

    # def _translate_dutyperiod(
    #     self,
    #     report_utc: datetime,
    #     next_report_lcl: str,
    #     s_dutyperiod: ST.DutyPeriod,
    # ) -> model.DutyPeriod:
    #     report_station = model.get_airport_code_from_iata(
    #         iata=s_dutyperiod.flights[0].departure_station
    #     )
    #     release_station = model.get_airport_code_from_iata(
    #         s_dutyperiod.flights[-1].arrival_station
    #     )
    #     duty = ST.parse_duration(s_dutyperiod.duty)
    #     release_utc = self._delta_dt(
    #         utc_ref=report_utc,
    #         td=duty,
    #         lcl_ref=s_dutyperiod.release_time.lcl,
    #         lcl_tz=release_station.tz_name,
    #         field_name="release",
    #     )
    #     flight_duty = ST.parse_duration(s_dutyperiod.flight_duty)
    #     operating_time = ST.parse_duration(s_dutyperiod.block)
    #     soft_time = ST.parse_duration(s_dutyperiod.synth)
    #     first_departure_delta = self._report_to_first_flight_delta(
    #         s_dutyperiod=s_dutyperiod
    #     )
    #     first_departure_utc = self._delta_dt(
    #         utc_ref=report_utc,
    #         td=first_departure_delta,
    #         lcl_ref=s_dutyperiod.flights[0].departure_time.lcl,
    #         lcl_tz=report_station.tz_name,
    #         field_name="First departure",
    #     )
    #     flights = self._translate_flights(
    #         first_departure_utc=first_departure_utc,
    #         s_flights=s_dutyperiod.flights,
    #     )
    #     layover = self._translate_layover(
    #         dutyperiod_release_utc=release_utc,
    #         next_report_lcl=next_report_lcl,
    #         s_layover=s_dutyperiod.layover,
    #     )
    #     flight_time = timedelta(
    #         seconds=sum([x.flight_time.total_seconds() for x in flights])
    #     )
    #     report_tzinfo = ZoneInfo(report_station.tz_name)
    #     report_lcl = utc_to_local(
    #         report_utc, report_tzinfo, s_dutyperiod.report_time.lcl
    #     )
    #     return model.DutyPeriod(
    #         report_station=report_station,
    #         report_utc=report_utc,
    #         report_lcl=report_lcl,
    #         report_hbt=report_utc.astimezone(self.hbt_tzinfo),
    #         release_station=release_station,
    #         release_utc=release_utc,
    #         release_lcl=release_utc.astimezone(ZoneInfo(release_station.tz_name)),
    #         release_hbt=release_utc.astimezone(self.hbt_tzinfo),
    #         flights=flights,
    #         duty=duty,
    #         flight_duty=flight_duty,
    #         flight_time=flight_time,
    #         operating_time=operating_time,
    #         soft_time=soft_time,
    #         layover=layover,
    #     )

    # def _translate_dutyperiods(
    #     self,
    #     first_report_utc: datetime,
    #     s_dutyperiods: Sequence[ST.DutyPeriod],
    # ) -> list[model.DutyPeriod]:
    #     dutyperiods: list[model.DutyPeriod] = []
    #     report_utc = first_report_utc
    #     for idx, s_dutyperiod in enumerate(s_dutyperiods, start=1):
    #         self.dp_idx = idx
    #         logger.debug(
    #             "Translating dutyperiod %d with report_utc %s",
    #             self.dp_idx,
    #             report_utc.isoformat(),
    #         )
    #         try:
    #             next_report_lcl = s_dutyperiods[idx].report_time.lcl
    #         except IndexError:
    #             next_report_lcl = ""
    #         dutyperiod = self._translate_dutyperiod(
    #             report_utc=report_utc,
    #             next_report_lcl=next_report_lcl,
    #             s_dutyperiod=s_dutyperiod,
    #         )
    #         dutyperiods.append(dutyperiod)
    #         if dutyperiod.layover is not None:
    #             report_utc = dutyperiod.release_utc + dutyperiod.layover.rest
    #     return dutyperiods

    # def _translate_layover(
    #     self,
    #     dutyperiod_release_utc: datetime,
    #     next_report_lcl: str,
    #     s_layover: ST.Layover | None,
    # ) -> model.Layover | None:
    #     if s_layover is None:
    #         logger.debug("No Layover.")
    #         return None
    #     logger.debug(
    #         "Translating layover with start %s", dutyperiod_release_utc.isoformat()
    #     )
    #     hotels = self._translate_hotels(s_hotels=s_layover.hotels)
    #     layover_station = model.get_airport_code_from_iata(iata=s_layover.city)

    #     rest = ST.parse_duration(s_layover.rest)
    #     end_utc = self._delta_dt(
    #         utc_ref=dutyperiod_release_utc,
    #         td=rest,
    #         lcl_ref=next_report_lcl,
    #         lcl_tz=layover_station.tz_name,
    #         field_name="Layover end",
    #     )
    #     return model.Layover(
    #         layover_station=layover_station,
    #         start_utc=dutyperiod_release_utc,
    #         start_lcl=dutyperiod_release_utc.astimezone(
    #             ZoneInfo(layover_station.tz_name)
    #         ),
    #         start_hbt=dutyperiod_release_utc.astimezone(self.hbt_tzinfo),
    #         end_utc=end_utc,
    #         end_lcl=end_utc.astimezone(ZoneInfo(layover_station.tz_name)),
    #         end_hbt=end_utc.astimezone(self.hbt_tzinfo),
    #         rest=rest,
    #         hotels=hotels,
    #     )

    # def _translate_hotel(self, s_hotel: ST.Hotel) -> model.Hotel:
    #     transportation: list[model.Transportation] = []
    #     for idx, s_trans in enumerate(s_hotel.transportation):
    #         logger.debug("Translating transportation %d", idx + 1)
    #         trans = model.Transportation(name=s_trans.name, phone=s_trans.phone)
    #         transportation.append(trans)
    #     hotel = model.Hotel(
    #         name=s_hotel.name, phone=s_hotel.phone, transportation=transportation
    #     )
    #     return hotel

    # def _translate_hotels(self, s_hotels: Sequence[ST.Hotel]) -> list[model.Hotel]:
    #     hotels: list[model.Hotel] = []
    #     for idx, s_hotel in enumerate(s_hotels):
    #         logger.debug("Translating hotel %d", idx + 1)
    #         hotels.append(self._translate_hotel(s_hotel=s_hotel))
    #     return hotels

    # def _translate_trip(
    #     self, s_trip: ST.StructuredTrip, start_date: date
    # ) -> model.ExpandedTrip:
    #     """Translate a StructuredTrip that starts on a particular date."""
    #     logger.info(
    #         "Translating trip %s - %s with start date %s uuid: %s",
    #         s_trip.number,
    #         s_trip.page_footer.base,
    #         start_date.isoformat(),
    #         self.s_trip.uuid,
    #     )
    #     # base_airport = model.get_airport_code_from_iata(s_trip.page_footer.base)
    #     first_report = time.fromisoformat(s_trip.dutyperiods[0].report_time.lcl)
    #     # Should be unambiguous unless start time is in the fold, Nov. dst switch 2am sunday.
    #     report_utc = datetime.combine(
    #         start_date, first_report, self.hbt_tzinfo
    #     ).astimezone(UTC)
    #     dutyperiods = self._translate_dutyperiods(
    #         first_report_utc=report_utc,
    #         s_dutyperiods=s_trip.dutyperiods,
    #     )
    #     positions = [model.Position(name=x) for x in s_trip.positions]
    #     operations = [model.Operation(name=x) for x in s_trip.operations]
    #     flight_time = timedelta(
    #         seconds=sum([x.flight_time.total_seconds() for x in dutyperiods])
    #     )
    #     operating_time = ST.parse_duration(s_trip.block)
    #     soft_time = ST.parse_duration(s_trip.synth)
    #     tafb = ST.parse_duration(s_trip.tafb)
    #     try:
    #         satellite_base = model.get_airport_code_from_iata(
    #             iata=s_trip.page_footer.satellite_base
    #         )
    #     except ValueError:
    #         satellite_base = None
    #     base_equipment = model.BaseEquipment(
    #         base=self.base,
    #         satellite_base=satellite_base,
    #         equipment=s_trip.page_footer.equipment,
    #     )
    #     return model.ExpandedTrip(
    #         source_uuid=s_trip.uuid,
    #         source_idx=s_trip.idx,
    #         trip_number=s_trip.number,
    #         base_equipment=base_equipment,
    #         positions=positions,
    #         operations=operations,
    #         special_qual=s_trip.special_qual,
    #         start_station=dutyperiods[0].report_station,
    #         start_utc=dutyperiods[0].report_utc,
    #         start_lcl=dutyperiods[0].report_lcl,
    #         start_hbt=dutyperiods[0].report_hbt,
    #         end_station=dutyperiods[-1].release_station,
    #         end_utc=dutyperiods[-1].release_utc,
    #         end_lcl=dutyperiods[-1].release_lcl,
    #         end_hbt=dutyperiods[-1].release_hbt,
    #         flight_time=flight_time,
    #         operating_time=operating_time,
    #         soft_time=soft_time,
    #         tafb=tafb,
    #         dutyperiods=dutyperiods,
    #     )

    # def _translate_trips(self, s_trip: ST.StructuredTrip) -> list[model.ExpandedTrip]:
    #     start_dates = ST.build_start_dates(
    #         effective_from=date.fromisoformat(s_trip.external.effective_from),
    #         effective_to=date.fromisoformat(s_trip.external.effective_to),
    #         calendar=s_trip.calendar,
    #     )
    #     trips: list[model.ExpandedTrip] = []
    #     for start_date in start_dates:
    #         trip = self._translate_trip(s_trip=s_trip, start_date=start_date)
    #         trips.append(trip)
    #     return trips

    # def _report_to_first_flight_delta(self, s_dutyperiod: ST.DutyPeriod) -> timedelta:
    #     """Get the delta between report and the first flight.

    #     report to first departure should be 1 hour or 30 min for dh leg.
    #     """
    #     if s_dutyperiod.flights[0].deadhead:
    #         td_delta = timedelta(minutes=30)
    #     else:
    #         td_delta = timedelta(hours=1)
    #     return td_delta

    # def _calculate_next_utc(
    #     self,
    #     utc_ref: datetime,
    #     td: timedelta,
    #     lcl_ref: str,
    #     lcl_tz: str,
    #     field_name: str,
    # ) -> datetime:
    #     simple_addition = utc_ref + td
    #     tzinfo = ZoneInfo(lcl_tz)
    #     next_time = time.fromisoformat(lcl_ref).replace(tzinfo=tzinfo)
    #     computed = next_local_time(dt_ref=utc_ref, next_time=next_time, delta=td)

    # def _delta_dt(
    #     self,
    #     utc_ref: datetime,
    #     td: timedelta,
    #     lcl_ref: str,
    #     lcl_tz: str,
    #     field_name: str,
    # ) -> datetime:
    #     """Get next utc time from uncertain info.

    #     Pbs pairing packages have some incorrect info sometimes.
    #     - during the nov. fold, a layover rest duration was an hour short when compared to release/report.

    #     figure out whether to use td addition, or next time calc to get accurate next utc.

    #     Args:
    #         utc_ref (datetime): _description_
    #         td (timedelta): _description_
    #         lcl_ref (str): _description_
    #         lcl_tz (str): _description_
    #         field_name (str): foo

    #     Returns:
    #         datetime: _description_
    #     """
    #     lcl_tzinfo = ZoneInfo(lcl_tz)

    #     dt_utc_addition = utc_ref + td
    #     dt_lcl_addition = dt_utc_addition.astimezone(lcl_tzinfo)
    #     if dt_lcl_addition.strftime("%H%M") == lcl_ref:
    #         return dt_utc_addition
    #     utc_ref_lcl = utc_ref.astimezone(lcl_tzinfo)
    #     dt_utc_next = next_local_time_in_utc(
    #         utc_start=utc_ref,
    #         next_lcl=time.fromisoformat(lcl_ref),
    #         next_tz_name=lcl_tz,
    #     )
    #     dt_lcl_next = dt_utc_next.astimezone(lcl_tzinfo)

    #     logger.info(
    #         "for dp: %d flt %d field: %s Delta addition did not match lcl_ref. ",
    #         self.dp_idx,
    #         self.flight_idx,
    #         field_name,
    #     )
    #     logger.info(
    #         "Inputs: utc_ref: %s, td: %s, lcl_ref: %s, lcl_tz: %s, utc_ref_lcl: %s ",
    #         utc_ref.isoformat(),
    #         td,
    #         lcl_ref,
    #         lcl_tz,
    #         utc_ref_lcl.isoformat(),
    #     )
    #     logger.info(
    #         "Addition: %s %s ", dt_utc_addition.isoformat(), dt_lcl_addition.isoformat()
    #     )
    #     logger.info(
    #         "Trying `next_local_time_in_utc`. %s %s",
    #         dt_utc_next.isoformat(),
    #         dt_lcl_next.isoformat(),
    #     )
    #     return dt_utc_next


def assemble_datetime(date_obj: date, time_str: str, tz_name: str) -> datetime:
    """Get the utc aware datetime from these inputs.

    Args:
        date_obj (date): _description_
        time_str (str): _description_
        tz_name (str): _description_

    Returns:
        datetime: The aware datetime in UTC.
    """
    tz_info = ZoneInfo(tz_name)
    time_local = time.fromisoformat(time_str)
    datetime_local = datetime.combine(date=date_obj, time=time_local, tzinfo=tz_info)
    return datetime_local.astimezone(UTC)


# def next_local_time_in_utc(
#     utc_start: datetime, next_lcl: time, next_tz_name: str
# ) -> datetime:
#     """Calculate the next occurance of a time in UTC.

#     Calulate the next occurance of a datetime in UTC when only the
#     following information is know.

#     This does not handle times `in the fold` of DST. eg november fall back.

#     Args:
#         utc_start (datetime): The datetime in UTC to reference
#         next_lcl (time): The local `time` that falls after `utc_start`
#         next_tz_name (str): The timezone name of `next_nieve`.

#     Returns:
#         datetime: The next datetime in UTC
#     """
#     local_tz = ZoneInfo(next_tz_name)
#     next_datetime = datetime.combine(
#         date=utc_start.astimezone(local_tz).date(),
#         time=next_lcl,
#         tzinfo=local_tz,
#     )
#     if next_datetime < utc_start.astimezone(local_tz):
#         # increment utc_start if `next_datetime` comes before a localized utc_start.
#         utc_start_increment = utc_start + timedelta(days=1)
#         next_datetime = datetime.combine(
#             date=utc_start_increment.astimezone(local_tz).date(),
#             time=next_lcl,
#             tzinfo=local_tz,
#         )
#     return next_datetime.astimezone(UTC)


def expand_trips(
    structured_trips: Iterable[ST.StructuredTrip],
    observer: Callable[[model.ExpandedTrip], None] | None = None,
) -> Iterator[model.ExpandedTrip]:
    """Expand structured trips, with an optional observer.

    Args:
        structured_trips (Iterable[ST.StructuredTrip]): _description_
        observer (Callable[[model.ExpandedTrip], None] | None, optional): _description_. Defaults to None.

    Yields:
        Iterator[model.ExpandedTrip]: _description_
    """
    for trip in structured_trips:
        expander = StructuredToExpanded(structured_trip=trip)
        expanded_trips = expander.translate()
        for expanded in expanded_trips:
            if observer:
                observer(expanded)
            yield expanded
