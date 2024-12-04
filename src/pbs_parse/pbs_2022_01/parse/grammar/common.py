"""Common elements for the pyparsing grammar."""

import pyparsing as pp

TIME = pp.Word(pp.nums, exact=4, as_keyword=True)
DUALTIME = pp.Combine(TIME("lcl") + pp.Literal("/") + TIME("hbt"))
DURATION = pp.Combine(pp.Word(pp.nums, min=1) + "." + pp.Word(pp.nums, exact=2))
CITY = pp.Word(pp.alphas, exact=3, as_keyword=True)
DASH_UNICODE = "\u002d\u2212"
MONTH_NUMERAL = pp.Word(pp.nums, exact=2)("month")
DAY_NUMERAL = pp.Word(pp.nums, exact=2)("day")
DASH_DAY = pp.Word(DASH_UNICODE, exact=2)
NUMERICAL_DAY = pp.MatchFirst(
    [
        pp.Word(pp.nums, exact=2, as_keyword=True),
        pp.Word(pp.nums, exact=1, as_keyword=True),
    ]
)
CALENDAR_DAY = pp.MatchFirst([DASH_DAY, NUMERICAL_DAY])
CALENDAR_LINE = pp.Opt(pp.OneOrMore(CALENDAR_DAY), default=[])("calendar_entries")
SHORT_MONTH = pp.Word(pp.alphas, exact=3)
DATE_DDMMM = MONTH_NUMERAL + SHORT_MONTH
YEAR = pp.Word(pp.nums, exact=4)
DATE_DDMMMYY = pp.Combine(DAY_NUMERAL + SHORT_MONTH + YEAR)


def trim_name(s: str, loc: int, tokens: pp.ParseResults) -> str:
    """Strip the leading and trailing white space."""
    value: str = tokens[1]  # type: ignore
    return value.strip()


PHONE_NUMBER = pp.Word(pp.nums, min=4, as_keyword=True)
SKIP_TO_PHONE = pp.original_text_for(pp.SkipTo(PHONE_NUMBER))
SKIP_TO_PHONE.set_parse_action(trim_name)
SKIP_TO_CALENDAR = pp.original_text_for(pp.SkipTo(CALENDAR_DAY))
SKIP_TO_CALENDAR.set_parse_action(trim_name)
SKIP_TO_END = pp.original_text_for(pp.SkipTo(pp.string_end))
SKIP_TO_END.set_parse_action(trim_name)
SKIP_TO_DURATION = pp.original_text_for(pp.SkipTo(DURATION))
SKIP_TO_DURATION.set_parse_action(trim_name)
