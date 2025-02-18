"""Matches a dutyperiod release."""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_td

from .common import CALENDAR_LINE, CITY, SKIP_TO_CALENDAR, SKIP_TO_END, SKIP_TO_PHONE

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def process_parsed(
    s: str, loc: int, toks: pp.ParseResults
) -> grammar_td.HotelAdditional:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())

    return grammar_td.HotelAdditional(
        layover_city=toks.layover_city,  # type: ignore
        name=toks.hotel_name,  # type: ignore
        phone=toks.hotel_phone,  # type: ignore
        calendar_entries=toks.calendar_entries.as_list(),  # type: ignore
    )


HotelAdditionalPhone = (
    pp.StringStart()
    + pp.Literal("+")
    + CITY("layover_city")
    + pp.WordEnd()
    + SKIP_TO_PHONE("hotel_name")
    + SKIP_TO_CALENDAR("hotel_phone")
    + CALENDAR_LINE("calendar_entries")
    + pp.StringEnd()
)
"""Has a phone number and optional calendar."""

HotelAdditionalNoPhone = (
    pp.StringStart()
    + pp.Literal("+")
    + CITY("layover_city")
    + pp.WordEnd()
    + SKIP_TO_CALENDAR("hotel_name")
    + CALENDAR_LINE("calendar_entries")
    + pp.StringEnd()
)
"""Has no phone number, has calendar."""
HotelAdditionalNone = (
    pp.StringStart()
    + pp.Literal("+")
    + CITY("layover_city")
    + pp.WordEnd()
    + SKIP_TO_END("hotel_name")
    + CALENDAR_LINE("calendar_entries")  # Just to include empty list in result.
    + pp.StringEnd()
)
"""Has no phone number or calendar."""
hotel_additional = pp.MatchFirst(
    [HotelAdditionalPhone, HotelAdditionalNoPhone, HotelAdditionalNone]
).set_parse_action(process_parsed)
"""
Matches:
```
               +PHL MARRIOTT OLD CITY                       12152386000
               +PHL CAMBRIA HOTEL AND SUITES                12157325500
```
"""
