"""Parse an iso8601 duration to timedelta.

https://github.com/gweis/isodate
https://en.wikipedia.org/wiki/ISO_8601

Durations define the amount of intervening time in a time interval and are represented
by the format P[n]Y[n]M[n]DT[n]H[n]M[n]S or P[n]W.
"""

import re
from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from typing import TypedDict

from pbs_parse.snippets.datetime.constants import (
    SECONDS_IN_DAY,
    SECONDS_IN_HOUR,
    SECONDS_IN_MINUTE,
    SECONDS_IN_WEEK,
)

ISO8601_PERIOD_REGEX = re.compile(
    r"^(?P<sign>[+-])?"
    r"P(?!\b)"
    r"(?P<years>[0-9]+([,.][0-9]+)?Y)?"
    r"(?P<months>[0-9]+([,.][0-9]+)?M)?"
    r"(?P<weeks>[0-9]+([,.][0-9]+)?W)?"
    r"(?P<days>[0-9]+([,.][0-9]+)?D)?"
    r"((?P<separator>T)(?P<hours>[0-9]+([,.][0-9]+)?H)?"
    r"(?P<minutes>[0-9]+([,.][0-9]+)?M)?"
    r"(?P<seconds>[0-9]+([,.][0-9]+)?S)?)?$"
)
"""Regular expression to parse ISO duration strings.

Matches fractional values using either `.` or `,`.

Note: the iso8601 spec only allows a fractional value for the lowest
value. eg. days for a duration with years and days.

https://github.com/gweis/isodate
"""


def is_ambiguous_duration(dur: str) -> bool:
    """Iso8601 durations with years or months are ambiguous.

    Leap years and variable length months are not accounted for.

    There are two possible M values, with a possible T separator.

    P1MT3H - ambiguous
    PT3M
    P1MT3M - ambiguous
    P1DT3H

    Args:
        dur (str): _description_

    Returns:
        bool: _description_
    """
    if "Y" in dur:
        return True
    split = dur.split("T")
    if len(split) > 1:
        if "M" in split[0]:
            # if there is a month value then it's ambiguous.
            return True
        else:
            return False
    elif "M" in dur:
        # if there is a month value then it's ambiguous.
        return True
    return False


@dataclass(slots=True, frozen=True)
class ParsedISODuration:
    """A container for an ISO8601 parsed duration.

    Supports conversion to timedelta.
    """

    sign: str | None
    years: str | None
    months: str | None
    weeks: str | None
    days: str | None
    separator: str | None
    hours: str | None
    minutes: str | None
    seconds: str | None
    original_str: str = ""

    def is_negative(self) -> bool:
        """is_negative.

        Returns:
            bool: _description_
        """
        if self.sign == "-":
            return True
        return False

    def is_ambiguous(self) -> bool:
        """is_ambiguous.

        Returns:
            bool: _description_
        """
        if any((self.years is not None, self.months is not None)):
            return True
        return False

    @staticmethod
    def from_isoformat(value: str) -> "ParsedISODuration":
        """from_isoformat.

        Args:
            value (str): _description_

        Returns:
            ParsedISODuration: _description_
        """
        parsed = parse_iso_duration(dur=value)
        return ParsedISODuration(**parsed, original_str=value)

    def to_timedelta(
        self, days_in_year: int | None = 365, days_in_month: int | None = None
    ) -> timedelta:
        """to_timedelta.

        Args:
            days_in_year (int | None, optional): _description_. Defaults to 365.
            days_in_month (int | None, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            timedelta: _description_
        """
        if all((self.years is not None, days_in_year is None)):
            raise ValueError(
                f"Not enough information to convert to timedelta. {days_in_year=}, {self!r}"
            )
        if all((self.months is not None, days_in_month is None)):
            raise ValueError(
                f"Not enough information to convert to timedelta. {days_in_month=}, {self!r}"
            )
        days, hours, minutes = 0, 0, 0
        if self.seconds is not None:
            seconds = Decimal(self.seconds)
        else:
            seconds = Decimal(0)
        if self.years is not None:
            assert days_in_year is not None
            if "." in self.years:
                whole, fraction = self.years.split(".", maxsplit=1)
                days = days + (int(whole) * days_in_year)
                year_seconds = Decimal(f"0.{fraction}") * (
                    SECONDS_IN_DAY * days_in_year
                )
                seconds = seconds + year_seconds
            else:
                days = days + (int(self.years) * days_in_year)
        if self.months is not None:
            assert days_in_month is not None
            if "." in self.months:
                whole, fraction = self.months.split(".", maxsplit=1)
                days = days + (int(whole) * days_in_month)
                month_seconds = (
                    Decimal(f"0.{fraction}") * days_in_month * SECONDS_IN_DAY
                )
                seconds = seconds + month_seconds
            else:
                days = days + (int(self.months) * days_in_month)
        if self.weeks is not None:
            if "." in self.weeks:
                whole, fraction = self.weeks.split(".", maxsplit=1)
                days = days + (int(whole) * 7)
                week_seconds = Decimal(f"0.{fraction}") * SECONDS_IN_WEEK
                seconds = seconds + week_seconds
            else:
                days = days + (int(self.weeks) * 7)
        if self.days is not None:
            if "." in self.days:
                whole, fraction = self.days.split(".", maxsplit=1)
                days = days + int(whole)
                day_seconds = Decimal(f"0.{fraction}") * SECONDS_IN_DAY
                seconds = seconds + day_seconds
            else:
                days = days + int(self.days)
        if self.hours is not None:
            seconds = seconds + (Decimal(self.hours) * SECONDS_IN_HOUR)
        if self.minutes is not None:
            seconds = seconds + (Decimal(self.minutes) * SECONDS_IN_MINUTE)
        td = timedelta(days=days, hours=hours, minutes=minutes, seconds=float(seconds))
        if self.is_negative():
            return timedelta(0) - td
        return td


def isoformat_to_timedelta(value: str) -> timedelta:
    """isoformat_to_timedelta.

    Args:
        value (str): _description_

    Returns:
        timedelta: _description_
    """
    parsed = ParsedISODuration.from_isoformat(value=value)
    return parsed.to_timedelta()


class ParsedISODurationTD(TypedDict):
    """The output of the iso8601 duration regex."""

    sign: str | None
    years: str | None
    months: str | None
    weeks: str | None
    days: str | None
    separator: str | None
    hours: str | None
    minutes: str | None
    seconds: str | None


def parse_iso_duration(dur: str) -> ParsedISODurationTD:
    """string_to_dict _summary_.

    Args:
        dur (str): _description_

    Examples:
        >>> dur = "P1Y2.3MT2H"
        >>> string_to_dict(dur)
        {
            'sign': None,
            'years': '1',
            'months': '2.3',
            'weeks': None,
            'days': None,
            'separator': 'T',
            'hours': '2',
            'minutes': None,
            'seconds': None
        }


    Returns:
        ParsedISODuration: _description_
    """
    match = ISO8601_PERIOD_REGEX.match(dur)
    if not match:
        raise ValueError(f"Could not parse {dur} as an iso8601 duration.")
    groups = match.groupdict()
    parsed = ParsedISODurationTD(
        sign=groups["sign"],
        years=groups["years"],
        months=groups["months"],
        weeks=groups["weeks"],
        days=groups["days"],
        separator=groups["separator"],
        hours=groups["hours"],
        minutes=groups["minutes"],
        seconds=groups["seconds"],
    )
    for key, value in parsed.items():
        if key not in ("separator", "sign"):
            if value is not None:
                # Strip unit character, and use . for decimal separator.
                parsed[key] = value[:-1].replace(",", ".")  # type: ignore

    return parsed


if __name__ == "__main__":
    from rich import print

    test_values = ["P1Y2.3MT2H", "PT4H2.34567S", "P23Y"]

    for value in test_values:
        print(f"String to parse: {value}")
        parsedTD = parse_iso_duration("P1Y2.3MT2H")
        print("TypeDict:")
        print(parsedTD)
        print("DataClass:")
        parsedDC = ParsedISODuration.from_isoformat(value=value)
        print(parsedDC)
        print("to timedelta:")
        try:
            print(repr(parsedDC.to_timedelta()))
        except ValueError as e:
            print(e)
        print()
