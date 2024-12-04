"""get leading whitespace."""

import re


def get_leading_whitespace(txt: str) -> str:
    """Get the leading whitespace of a string."""
    # TODO move to snippet
    # https://stackoverflow.com/a/2268559/105844
    matched = re.match(r"\s*", txt)
    if matched is None:
        return ""
    return matched.group()
