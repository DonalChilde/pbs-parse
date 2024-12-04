"""Matches a trip footer."""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_TD

from .common import CALENDAR_LINE, DURATION

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def process_parsed(s: str, loc: int, toks: pp.ParseResults) -> grammar_TD.TripFooter:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())

    return grammar_TD.TripFooter(
        block=toks.block,  # type: ignore
        synth=toks.synth,  # type: ignore
        total_pay=toks.total_pay,  # type: ignore
        tafb=toks.tafb,  # type: ignore
        calendar_entries=toks.calendar_entries.as_list(),  # type: ignore
    )


trip_footer = (
    pp.StringStart()
    + "TTL"
    + DURATION("block")
    + DURATION("synth")
    + DURATION("total_pay")
    + DURATION("tafb")
    + CALENDAR_LINE("calendar_entries")
    + pp.StringEnd()
).set_parse_action(process_parsed)
"""
Matches:
```
TTL                                              7.50   0.00   7.50        10.20       −− −− −−

```
"""
