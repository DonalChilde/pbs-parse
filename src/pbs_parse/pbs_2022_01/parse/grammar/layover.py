"""Matches a dutyperiod report."""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_TD

from .common import (
    CALENDAR_LINE,
    CITY,
    DURATION,
    PHONE_NUMBER,
    SKIP_TO_DURATION,
    SKIP_TO_PHONE,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def process_parsed(s: str, loc: int, toks: pp.ParseResults) -> grammar_TD.Layover:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())

    return grammar_TD.Layover(
        layover_city=toks.layover_city,  # type: ignore
        hotel_name=toks.hotel_name,  # type: ignore
        hotel_phone=toks.hotel_phone,  # type: ignore
        rest=toks.rest,  # type: ignore
        calendar_entries=toks.calendar_entries.as_list(),  # type: ignore
    )


LayoverPhone = (
    pp.StringStart()
    + CITY("layover_city")
    + SKIP_TO_PHONE("hotel_name")
    + PHONE_NUMBER("hotel_phone")
    + DURATION("rest")
    + CALENDAR_LINE("calendar_entries")
    + pp.StringEnd()
)
LayoverNoPhone = (
    pp.StringStart()
    + CITY("layover_city")
    + pp.Opt(SKIP_TO_DURATION("hotel_name"))
    + DURATION("rest")
    + CALENDAR_LINE("calendar_entries")
    + pp.StringEnd()
)

layover = pp.MatchFirst([LayoverPhone, LayoverNoPhone]).set_parse_action(process_parsed)
"""
```
Matches:
                MIA SONESTA MIAMI AIRPORT                   13054469000    11.27       −− −− −− −− −− −− −−
                LHR PARK PLAZA WESTMINSTER BRIDGE LONDON    443334006112   24.00       −− −− −− −− −− −− −−
```
"""
