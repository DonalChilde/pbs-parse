"""Parse an iso8601 duration to timedelta.

https://github.com/gweis/isodate
https://en.wikipedia.org/wiki/ISO_8601

Durations define the amount of intervening time in a time interval and are represented
by the format P[n]Y[n]M[n]DT[n]H[n]M[n]S or P[n]W.
"""

import re
from datetime import timedelta
from typing import TypedDict

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
            return True
    elif "M" in dur:
        return True
    return False


def string_to_timedelta(dur: str, ambiguous_duration_fail: bool = True) -> timedelta:
    """string_to_timedelta _summary_.

    Args:
        dur (str): An iso8601 duration string.
        ambiguous_duration_fail (bool): Raise an exception for an ambiguous duration. Defaults to True.

    Returns:
        timedelta: _description_
    """
    if ambiguous_duration_fail:
        if is_ambiguous_duration(dur=dur):
            raise ValueError(
                f"Year and month values cannot be turned into a consistent duration. {dur}"
            )
    matches: Duration = string_to_dict(dur=dur)
    negative = "-" in matches.get("sign")
    ret_value = timedelta(
        weeks=float(matches["weeks"]),
        days=float(matches["days"]),
        hours=float(matches["hours"]),
        minutes=float(matches["minutes"]),
        seconds=float(matches["seconds"]),
    )
    if negative:
        return timedelta(0) - ret_value
    return ret_value


class Duration(TypedDict):
    """The output of the iso8601 duration regex."""

    sign: str
    years: str
    months: str
    weeks: str
    days: str
    separator: str
    hours: str
    minutes: str
    seconds: str


def string_to_dict(dur: str) -> Duration:
    """string_to_dict _summary_.

    Args:
        dur (str): _description_

    Examples:
        >>> dur = "P1Y2.3MT2H"
        >>> string_to_dict(dur)
        {
            'sign': '',
            'years': '1',
            'months': '2.3',
            'weeks': '0',
            'days': '0',
            'separator': 'T',
            'hours': '2',
            'minutes': '0',
            'seconds': '0'
        }



    Returns:
        dict[str,str]: _description_
    """
    match = ISO8601_PERIOD_REGEX.match(dur)
    if not match:
        raise ValueError(f"Could not parse {dur} as an iso8601 duration.")
    groups = match.groupdict()
    # clean the matches
    if groups["sign"] is None:
        groups["sign"] = ""
    for key, val in groups.items():
        if key not in ("separator", "sign"):
            if val is None:
                # a default value to make parsing to number easier.
                groups[key] = "0n"
            groups[key] = groups[key][:-1].replace(",", ".")

    return groups  # type: ignore


def timedelta_to_isoformat(td: timedelta) -> str:
    """timedelta_to_isoformat.

    Args:
        td (timedelta): _description_

    Returns:
        str: _description_
    """
    negative = td < timedelta(0)
    abs_value = abs(td)
    days, rem = divmod(abs_value, timedelta(days=1))
    hours, rem = divmod(rem, timedelta(hours=1))
    minutes, rem = divmod(rem, timedelta(minutes=1))
    seconds = int(rem.total_seconds())
    microseconds = rem.microseconds
    if negative:
        sign = "-"
    else:
        sign = ""
    output = [sign, "P"]
    has_HMS = False
    if days > 0:
        output.append(f"{days}D")
    if hours > 0:
        output.append("T")
        output.append(f"{hours}H")
        has_HMS = True
    if minutes > 0:
        if not has_HMS:
            output.append("T")
            has_HMS = True
        output.append(f"{minutes}M")
    if seconds > 0:
        if not has_HMS:
            output.append("T")
            has_HMS = True
        output.append(f"{seconds}")
        if microseconds > 0:
            output.append(f".{str(microseconds).zfill(6)}")
        output.append("S")
    if seconds == 0 and microseconds > 0:
        if not has_HMS:
            output.append("T")
            has_HMS = True
        output.append(f"0.{str(microseconds).zfill(6)}S")
    return "".join(output)
