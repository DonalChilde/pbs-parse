"""Matches the base equipment line that comes just after the two page header lines.

This line occurs once for each base equipment change.
While the sections are not really labeled, the first page with PHX 737 trips
will have this line. The first page with PHX 320 trips will then have this line.
Note. This info is also mirrored in each page footer.


"""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_td

from .common import CITY

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def process_parsed(s: str, loc: int, toks: pp.ParseResults) -> grammar_td.BaseEquipment:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())
    return grammar_td.BaseEquipment(
        base=toks.base,  # type: ignore
        satellite_base=toks.satellite_base,  # type: ignore
        equipment=toks.equipment,  # type: ignore
    )


base_equipment = (
    pp.StringStart()
    + CITY("base")
    + pp.Opt(CITY("satellite_base"))
    + pp.Word(pp.nums, exact=3)("equipment")
    + pp.StringEnd()
).set_parse_action(process_parsed)
"""
Matches:
```
BOS 737
LAX SAN 737
```
"""
