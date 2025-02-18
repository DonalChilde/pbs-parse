"""Matches the second page header line.

The first page header line line has no useful data.
This line has the from and to date for the calendar.

Matches:
```
DP D/A EQ FLT#  STA DLCL/DHBT ML STA ALCL/AHBT  BLOCK  SYNTH   TPAY   DUTY  TAFB   FDP CALENDAR 05/02−06/01
```
"""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_td

from .common import DASH_UNICODE, DAY_NUMERAL, MONTH_NUMERAL

logger = logging.getLogger(__name__)
DATE_MM_SLASH_DD = MONTH_NUMERAL + "/" + DAY_NUMERAL


def process_parsed(s: str, loc: int, toks: pp.ParseResults) -> grammar_td.PageHeader2:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())
    return grammar_td.PageHeader2(
        from_date=grammar_td.MonthDay(month=toks.from_date[0], day=toks.from_date[2]),  # type: ignore
        to_date=grammar_td.MonthDay(month=toks.to_date[0], day=toks.to_date[2]),  # type: ignore
    )


page_header_2 = (
    pp.StringStart()
    + pp.SkipTo("CALENDAR", include=True)
    + DATE_MM_SLASH_DD("from_date")
    + pp.Word(DASH_UNICODE)
    + DATE_MM_SLASH_DD("to_date")
    + pp.StringEnd()
).set_parse_action(process_parsed)
"""
Matches:
```
DP D/A EQ FLT#  STA DLCL/DHBT ML STA ALCL/AHBT  BLOCK  SYNTH   TPAY   DUTY  TAFB   FDP CALENDAR 05/02−06/01
```
"""
