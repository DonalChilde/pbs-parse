"""Matches a trip header."""

import logging

import pyparsing as pp

from pbs_parse.pbs_2022_01.models import grammar_TD

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

POSITIONS = pp.one_of("CA FO FB C RC", as_keyword=True)
SPECIAL_QUAL = pp.Literal("SPECIAL") + "QUALIFICATION"
CALENDAR_HEADER = pp.Literal("MO") + "TU" + "WE" + "TH" + "FR" + "SA" + "SU"


def process_parsed(s: str, loc: int, toks: pp.ParseResults) -> grammar_TD.TripHeader:
    """Process the parsed data."""
    logger.debug("%s -> %s", s, toks.dump())
    if toks.special_qual[0] == False:  # type: ignore
        special_qual = False
    else:
        special_qual = True
    if "prior" in toks.calendar_header.as_list():  # type: ignore
        prior_month_trip = True
    else:
        prior_month_trip = False
    return grammar_TD.TripHeader(
        trip_number=toks.number,  # type: ignore
        ops_count=toks.ops_count,  # type: ignore
        positions=toks.positions.as_list(),  # type: ignore
        operations=toks.operations.as_list(),  # type: ignore
        special_qual=special_qual,
        prior_month_trip=prior_month_trip,
    )


trip_header = (
    pp.StringStart()
    + "SEQ"
    + pp.Word(pp.nums, min=1, as_keyword=True)("number")
    + pp.Word(pp.nums, min=1, as_keyword=True)("ops_count")
    + "OPS"
    + "POSN"
    + pp.OneOrMore(POSITIONS)("positions")
    + pp.Opt("ONLY")
    + pp.Opt(
        pp.ZeroOrMore(pp.Word(pp.printables, as_keyword=False), stop_on="OPERATION")
        + pp.Suppress("OPERATION"),
        default=list(),
    )("operations")
    # + pp.Opt(SPECIAL_QUAL, default=False)("special_qual").set_parse_action(
    #     lambda tokens: bool(tokens.as_dict().get("special_qual", False))
    # )
    + pp.Opt(SPECIAL_QUAL, default=False)("special_qual")
    # + pp.Opt(
    #     pp.ZeroOrMore(pp.Word(pp.printables, as_keyword=True), stop_on="QUALIFICATION")
    #     + pp.Suppress("QUALIFICATION"),
    #     default=list(),
    # )("special_qual")
    + pp.MatchFirst(
        [
            CALENDAR_HEADER,
            (
                pp.one_of(["Replaces", "New"])
                + "prior"
                + "month"
                + pp.Optional("deadhead")
            ),
        ]
    )("calendar_header")
    + pp.StringEnd()
).set_parse_action(process_parsed)
"""
Matches:
```
SEQ 25064   1 OPS   POSN CA FO                                                         MO TU WE TH FR SA SU
SEQ 6292    1 OPS   POSN CA FO                SPANISH OPERATION                        MO TU WE TH FR SA SU
SEQ 16945   1 OPS   POSN CA FO                SPECIAL QUALIFICATION                    MO TU WE TH FR SA SU
SEQ 30569   1 OPS   POSN CA FO                                                         New prior month
SEQ 30890   1 OPS   POSN CA FO                                                         Replaces prior month
SEQ 19448   1 OPS   POSN CA FO                ST. THOMAS OPERATION                     MO TU WE TH FR SA SU
SEQ 265    10 OPS   POSN FB ONLY              GERMAN   OPERATION                       MO TU WE TH FR SA SU
SEQ 264     4 OPS   POSN FB ONLY                                                       MO TU WE TH FR SA SU
SEQ 657     2 OPS   POSN FO C                                                          MO TU WE TH FR SA SU
SEQ 30097   1 OPS   POSN FB ONLY              JAPANESE OPERATION                       Replaces prior month
```
"""
