"""Matches a calendar only line."""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_TD

from .common import CALENDAR_LINE

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def process_parsed(s: str, loc: int, toks: pp.ParseResults) -> grammar_TD.CalendarOnly:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())

    return grammar_TD.CalendarOnly(calendar_entries=toks.calendar_entries.as_list())  # type: ignore


calendar_only = pp.StringStart() + CALENDAR_LINE("calendar_entries") + pp.StringEnd()
calendar_only.set_parse_action(process_parsed)
"""
Matches:
```
                                                                                       −− 17 18 19 20 21 22
                                                                                       23 24 25 26 27 28 29
```
"""
