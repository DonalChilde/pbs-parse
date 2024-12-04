"""Matches a flight."""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_TD
from pbs_parse.pbs_2022_01.parse.grammar_2.common import (
    CALENDAR_LINE,
    CITY,
    DUALTIME,
    DURATION,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

POSITIONS = pp.one_of("CA FO FB C RC", as_keyword=True)
SPECIAL_QUAL = pp.Literal("SPECIAL") + "QUALIFICATION"
CALENDAR_HEADER = pp.Literal("MO") + "TU" + "WE" + "TH" + "FR" + "SA" + "SU"


def process_parsed_flight(s: str, loc: int, toks: pp.ParseResults) -> grammar_TD.Flight:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())

    return grammar_TD.Flight(
        dutyperiod_idx=toks.dutyperiod_idx,  # type: ignore
        depart_day=toks.depart_day,  # type: ignore
        arrive_day=toks.arrive_day,  # type: ignore
        equipment_code=toks.equipment_code,  # type: ignore
        flight_number=toks.flight_number,  # type: ignore
        deadhead=False,
        deadhead_code="",
        departure_station=toks.departure_station,  # type: ignore
        departure_time=grammar_TD.DualTime(
            lcl=toks.departure_time.lcl,  # type: ignore
            hbt=toks.departure_time.hbt,  # type: ignore
        ),
        crew_meal=toks.crewmeal,  # type: ignore
        arrival_station=toks.arrival_station,  # type: ignore
        arrival_time=grammar_TD.DualTime(
            lcl=toks.arrival_time.lcl,  # type: ignore
            hbt=toks.arrival_time.hbt,  # type: ignore
        ),
        block=toks.block,  # type: ignore
        synth="0.00",  # type: ignore
        ground=toks.ground,  # type: ignore
        equipment_change=bool(toks.equipment_change),  # type: ignore
        calendar_entries=toks.calendar_entries.as_list(),  # type: ignore
    )


flight = (
    pp.StringStart()
    + pp.Word(pp.nums, exact=1, as_keyword=True)("dutyperiod_idx")
    + pp.Word(pp.nums, exact=1)("depart_day")
    + pp.Literal("/")
    + pp.Word(pp.nums, exact=1)("arrive_day")
    + pp.Word(pp.alphanums, exact=2, as_keyword=True)("equipment_code")
    + pp.Word(pp.nums)("flight_number")
    + CITY("departure_station")
    + DUALTIME("departure_time")
    + pp.Opt(pp.Word(pp.alphas, exact=1, as_keyword=True), default="")("crew_meal")
    + CITY("arrival_station")
    + DUALTIME("arrival_time")
    + DURATION("block")
    # FIXME synth time? Can this happen on a non deadhead?
    + pp.Opt(DURATION("ground"), default="0.00")
    + pp.Opt("X", default="")("equipment_change")
    + CALENDAR_LINE
    + pp.StringEnd()
).set_parse_action(process_parsed_flight)
"""
Matches:
```
1  1/1 65 2131  SAN 1337/1337    ORD 1935/1735   3.58          1.10X                   −− −− −− −− −− −− −−


```
"""


def process_parsed_flight_deadhead(
    s: str, loc: int, toks: pp.ParseResults
) -> grammar_TD.Flight:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())

    return grammar_TD.Flight(
        dutyperiod_idx=toks.dutyperiod_idx,  # type: ignore
        depart_day=toks.depart_day,  # type: ignore
        arrive_day=toks.arrive_day,  # type: ignore
        equipment_code=toks.equipment_code,  # type: ignore
        flight_number=toks.flight_number,  # type: ignore
        deadhead=True,
        deadhead_code=toks.deadhead_code,  # type: ignore
        departure_station=toks.departure_station,  # type: ignore
        departure_time=grammar_TD.DualTime(
            lcl=toks.departure_time.lcl,  # type: ignore
            hbt=toks.departure_time.hbt,  # type: ignore
        ),
        crew_meal=toks.crewmeal,  # type: ignore
        arrival_station=toks.arrival_station,  # type: ignore
        arrival_time=grammar_TD.DualTime(
            lcl=toks.arrival_time.lcl,  # type: ignore
            hbt=toks.arrival_time.hbt,  # type: ignore
        ),
        block="0.00",  # type: ignore
        synth=toks.synth,  # type: ignore
        ground=toks.ground,  # type: ignore
        equipment_change=bool(toks.equipment_change),  # type: ignore
        calendar_entries=toks.calendar_entries.as_list(),  # type: ignore
    )


flight_deadhead = (
    pp.StringStart()
    + pp.Word(pp.nums, exact=1, as_keyword=True)("dutyperiod_idx")
    + pp.Word(pp.nums, exact=1)("depart_day")
    + pp.Literal("/")
    + pp.Word(pp.nums, exact=1)("arrive_day")
    + pp.Word(pp.alphanums, exact=2, as_keyword=True)("equipment_code")
    + pp.Word(pp.nums)("flight_number")
    + pp.Literal("D")("deadhead")
    + pp.WordEnd()
    + CITY("departure_station")
    + DUALTIME("departure_time")
    + pp.Opt(pp.Word(pp.alphas, exact=1, as_keyword=True), default="")("crew_meal")
    + CITY("arrival_station")
    + DUALTIME("arrival_time")
    + pp.Word(pp.alphas, exact=2)("deadhead_code")
    + DURATION("synth")
    + pp.Opt(DURATION("ground"), default="0.00")
    + pp.Opt("X", default="")("equipment_change")
    + CALENDAR_LINE
    + pp.StringEnd()
).set_parse_action(process_parsed_flight_deadhead)
"""
Matches:
```
3  3/3 CE 2308D DFW 1635/1635    AUS 1741/1741    AA    1.06
2  2/2 45 1614D MCI 1607/1407    DFW 1800/1600    AA    1.53   1.27X
4  4/4 64 2578D MIA 1949/1649    SAN 2220/2220    AA    5.31
```
"""
