"""Matches a dutyperiod release."""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_TD

from .common import CALENDAR_LINE, DUALTIME, DURATION

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def process_parsed(
    s: str, loc: int, toks: pp.ParseResults
) -> grammar_TD.DutyPeriodRelease:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())

    return grammar_TD.DutyPeriodRelease(
        release=grammar_TD.DualTime(lcl=toks.release.lcl, hbt=toks.release.hbt),  # type: ignore
        block=toks.block,  # type: ignore
        synth=toks.synth,  # type: ignore
        total_pay=toks.total_pay,  # type: ignore
        duty=toks.duty,  # type: ignore
        flight_duty=toks.flight_duty,  # type: ignore
        calendar_entries=toks.calendar_entries.as_list(),  # type: ignore
    )


dutyperiod_release = (
    pp.StringStart()
    + "RLS"
    + DUALTIME("release")
    + DURATION("block")
    + DURATION("synth")
    + DURATION("total_pay")
    + DURATION("duty")
    + DURATION("flight_duty")
    + CALENDAR_LINE("calendar_entries")
    + pp.StringEnd()
).set_parse_action(process_parsed)
"""
Matches:
```
                                 RLS 0739/0439   4.49   0.00   4.49   6.19        5.49 −− −− −− −− −− −− −−
                                 RLS 2252/2252   0.00   5.46   5.46   6.46        0.00
```
"""
