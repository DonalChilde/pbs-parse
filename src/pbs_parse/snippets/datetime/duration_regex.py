"""Various duration parsing strategies using regex."""

from re import Pattern, compile

# HHH = r"(?P<hours>[0-9]+([,.][0-9]+)?)" # only matches 1,000, not 1,000,000
HHH = r"(?P<hours>[0-9]+)"
MM = r"(?P<minutes>[0-5][0-9])"
SS = r"(?P<seconds>[0-5][0-9])"
FS = r"(?P<fractional_seconds>([0-9]+))"

# TODO tests and examples
# TODO parse larger numbers with commas?


def pattern_HHHMMSSFS(
    hm_sep: str = ":", ms_sep: str = ":", fs_sep: str = "."
) -> Pattern[str]:
    """Parse a string duration of the pattern HHHMMSSFS.

    Some valid formats:
    0:00:01
    123:14:35
    123:15:34.456

    _extended_summary_

    Args:
        hm_sep: _description_. Defaults to ":".
        ms_sep: _description_. Defaults to ":".
        fs_sep: _description_. Defaults to ".".

    Returns:
        _description_
    """
    pattern_string = rf"{HHH}{hm_sep}{MM}{ms_sep}{SS}({fs_sep}{FS})?"
    return compile(pattern_string)


def pattern_HHHMM(hm_sep: str = ":") -> Pattern[str]:
    """A regex pattern to match simple duration strings.

    The separator between HHH and MM can be customized.

    Args:
        hm_sep: The separator between HHH and MM. Defaults to ":".

    Returns:
        The complied pattern for the regex.

    Examples:
        >>> match = pattern_HHHMM(".").fullmatch("234.45")
        >>> match.groupdict()
        {'hours': '234', 'minutes': '45'}

        >>> match = pattern_HHHMM().fullmatch("234:45")
        >>> match.groupdict()
        {'hours': '234', 'minutes': '45'}

        >>> match = pattern_HHHMM().fullmatch("1234:45")
        >>> match.groupdict()
        {'hours': '1234', 'minutes': '45'}
    """
    pattern_string = rf"{HHH}{hm_sep}{MM}"
    return compile(pattern_string)
