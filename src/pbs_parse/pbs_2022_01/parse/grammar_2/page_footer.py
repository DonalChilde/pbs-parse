"""Matches a page footer."""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_TD

from .common import CITY, DATE_DDMMMYY

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def process_parsed(s: str, loc: int, toks: pp.ParseResults) -> grammar_TD.PageFooter:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())

    return grammar_TD.PageFooter(
        issued=toks.issued[0],  # type: ignore
        effective=toks.effective[0],  # type: ignore
        base=toks.base,  # type: ignore
        satellite_base=toks.satellite_base,  # type: ignore
        equipment=toks.equipment,  # type: ignore
        division=toks.division,  # type: ignore
        page=toks.page,  # type: ignore
    )


page_footer = (
    pp.StringStart()
    + "COCKPIT"
    + "ISSUED"
    + DATE_DDMMMYY("issued")
    + "EFF"
    + DATE_DDMMMYY("effective")
    + CITY("base")
    + pp.Opt(CITY, default="")("satellite_base")
    + pp.Word(pp.nums, exact=3)("equipment")
    + (pp.Literal("INTL") | pp.Literal("DOM"))("division")
    + "PAGE"
    + pp.Word(pp.nums)("page")
    + pp.StringEnd()
).set_parse_action(process_parsed)
"""
Matches:
```
COCKPIT  ISSUED 08APR2022  EFF 02MAY2022               LAX 737  DOM                              PAGE   644
COCKPIT  ISSUED 08APR2022  EFF 02MAY2022               LAX 320  INTL                             PAGE  1178
```
"""
