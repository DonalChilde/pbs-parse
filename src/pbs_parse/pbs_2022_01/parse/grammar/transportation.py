"""Matches a transportation."""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_TD

from .common import (
    CALENDAR_LINE,
    PHONE_NUMBER,
    SKIP_TO_CALENDAR,
    SKIP_TO_END,
    SKIP_TO_PHONE,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def process_parsed(
    s: str, loc: int, toks: pp.ParseResults
) -> grammar_TD.Transportation:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())

    if not (cal := toks.calendar_entries):  # type: ignore
        calendar_entries = []
    else:
        calendar_entries = cal.as_list()  # type: ignore

    return grammar_TD.Transportation(
        name=toks.transportation_name,  # type: ignore
        phone=toks.transportation_phone,  # type: ignore
        calendar_entries=calendar_entries,  # type: ignore
    )


TransportationPhone = (
    pp.StringStart()
    + pp.NotAny("+")
    + SKIP_TO_PHONE("transportation_name")
    + SKIP_TO_CALENDAR("transportation_phone")
    + CALENDAR_LINE("calendar_entries")
    + pp.StringEnd()
)
TransportationNoPhone = (
    pp.StringStart()
    + pp.NotAny("+")
    + SKIP_TO_CALENDAR("transportation_name")
    + CALENDAR_LINE("calendar_entries")
    + pp.StringEnd()
)
TransportationNoCal = (
    pp.StringStart()
    + pp.NotAny("+")
    + SKIP_TO_PHONE("transportation_name")
    + PHONE_NUMBER("transportation_phone")
    + pp.StringEnd()
)
TransportationNone = (
    pp.StringStart()
    + pp.NotAny("+")
    + SKIP_TO_END("transportation_name")
    # + CALENDAR_LINE("calendar_entries")  # Just to have empty list in results
    + pp.StringEnd()
)
transportation = pp.MatchFirst(
    [
        TransportationPhone,
        TransportationNoPhone,
        TransportationNoCal,
        TransportationNone,
    ]
).set_parse_action(process_parsed)
"""
Matches:
```
                    SIN FIN DE SERVICIOS                    3331223240
                    VIP TRANSPORTATION− OGG                 8088712702                 −− −− −−
```
"""


# transportation_additional = pp.MatchFirst(
#     [TransportationPhone, TransportationNoPhone, TransportationNone]
# ).set_parse_action(process_parsed)
# """
# Matches:
# ```
#                     SKY TRANSPORTATION SERVICE, LLC         8566169633
#                     DESERT COACH                            6022866161
# ```
# """
