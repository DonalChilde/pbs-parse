"""Matches a dutyperiod report."""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_td

from .common import CALENDAR_LINE, DATE_DDMMM, DUALTIME

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def process_parsed(
    s: str, loc: int, toks: pp.ParseResults
) -> grammar_td.DutyperiodReport:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())

    return grammar_td.DutyperiodReport(
        report=grammar_td.DualTime(lcl=toks.report.lcl, hbt=toks.report.hbt),  # type: ignore
        calendar_entries=toks.calendar_entries.as_list(),  # type: ignore
    )


dutyperiod_report = (
    pp.StringStart()
    + "RPT"
    + DUALTIME("report")
    + CALENDAR_LINE
    + pp.Opt(
        pp.Literal("sequence")
        + pp.Word(pp.nums, min=1)("sequence_number")
        + "/"
        + DATE_DDMMM("date")
    )
    + pp.Opt(pp.Literal("sequence") + DATE_DDMMM("date"))
    + pp.StringEnd()
).set_parse_action(process_parsed)
"""
Matches:
```
                RPT 1237/1237                                                           2 −− −− −− −− −− −−
                RPT 1000/1000                                                          sequence 25384/30DEC
                RPT 1829/1829                                                          sequence 01JUL

```
"""
