"""FILE: factored_timedelta.py."""

from dataclasses import dataclass
from datetime import timedelta

# YEAR = timedelta(days=365)
DAY = timedelta(days=1)
HOUR = timedelta(hours=1)
MINUTE = timedelta(minutes=1)
ZERO = timedelta(seconds=0)


@dataclass(slots=True)
class FactoredTimedelta:
    """FactoredTimedelta."""

    is_negative: bool = False
    # years: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    microseconds: int = 0

    def to_timedelta(self) -> timedelta:
        """Convert to timedelta."""
        # days = (self.years * 365) + self.days
        td = timedelta(
            days=self.days,
            hours=self.hours,
            minutes=self.minutes,
            seconds=self.seconds,
            microseconds=self.microseconds,
        )
        if self.is_negative:
            return ZERO - td
        return td

    @staticmethod
    def from_timedelta(td: timedelta) -> "FactoredTimedelta":
        """Convert timedelta to FactoredTimedelta."""
        return factor_time_delta(td=td)

    def to_isoformat(self) -> str:
        """Convert to iso format."""
        return factored_to_isoformat(factored=self)


def timedelta_to_isoformat(td: timedelta) -> str:
    """timedelta_to_isoformat.

    Args:
        td (timedelta): _description_

    Returns:
        str: _description_
    """
    factored = FactoredTimedelta.from_timedelta(td=td)
    return factored.to_isoformat()


def factor_time_delta(td: timedelta) -> FactoredTimedelta:
    """Factor a timedelta to a defined set of fields.

    Args:
        td (timedelta): _description_

    Returns:
        FactoredTimedelta: _description_
    """
    if td == ZERO:
        return FactoredTimedelta()
    is_negative = td < ZERO
    abs_value = abs(td)
    # years, rem = divmod(abs_value, YEAR)
    days, rem = divmod(abs_value, DAY)
    hours, rem = divmod(rem, HOUR)
    minutes, rem = divmod(rem, MINUTE)
    seconds = int(rem.total_seconds())
    microseconds = rem.microseconds
    return FactoredTimedelta(
        is_negative=is_negative,
        # years=years,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
    )


def factored_to_isoformat(factored: FactoredTimedelta) -> str:
    """factored_to_isoformat.

    Args:
        factored (FactoredTimedelta): _description_

    Returns:
        str: _description_
    """
    if all(
        [
            # factored.years == 0,
            factored.days == 0,
            factored.hours == 0,
            factored.minutes == 0,
            factored.seconds == 0,
            factored.microseconds == 0,
        ]
    ):
        return "PT0S"
    if factored.is_negative:
        sign = "-"
    else:
        sign = ""
    output = [sign, "P"]
    if any(
        [
            factored.hours > 0,
            factored.minutes > 0,
            factored.seconds > 0,
            factored.microseconds > 0,
        ]
    ):
        time_sep = "T"
    else:
        time_sep = ""
    if factored.days > 0:
        output.append(f"{factored.days}D")
    output.append(time_sep)
    if factored.hours > 0:
        output.append(f"{factored.hours}H")
    if factored.minutes > 0:
        output.append(f"{factored.minutes}M")
    if factored.seconds > 0:
        output.append(f"{factored.seconds}")
        if factored.microseconds > 0:
            output.append(f".{str(factored.microseconds).zfill(6)}")
        output.append("S")
    if factored.seconds == 0 and factored.microseconds > 0:
        output.append(f"0.{str(factored.microseconds).zfill(6)}S")
    return "".join(output)


if __name__ == "__main__":
    from rich import print

    neg = ZERO - timedelta(days=35)
    test_data = [
        timedelta(days=23, hours=2),
        timedelta(days=450, seconds=5.435),
        ZERO - timedelta(days=35),
        timedelta(seconds=75),
    ]
    for value in test_data:
        print(value)
        factored = FactoredTimedelta.from_timedelta(td=value)
        print(factored)
        print(factored.to_isoformat())
        print(factored.to_timedelta())
        print()
