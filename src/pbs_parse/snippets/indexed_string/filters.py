from typing import Callable, Sequence

from pbs_parse.snippets.indexed_string.protocols import IndexedStringProtocol


class SkipTillFirstMatch:
    """
    Skip until first match found.

    """

    def __init__(self, match_test: Callable[[IndexedStringProtocol], bool]) -> None:
        self.match_test = match_test
        self.procede = False

    def __call__(self, indexed_string: IndexedStringProtocol) -> bool:
        if self.procede:
            return True
        if self.match_test(indexed_string):
            self.procede = True
            return True
        return False


class MultipleTests:
    """Test for multiple conditions."""

    def __init__(
        self, testers: Sequence[Callable[[IndexedStringProtocol], bool]]
    ) -> None:
        self.testers: Sequence[Callable[[IndexedStringProtocol], bool]] = list(testers)

    def __call__(self, indexed_string: IndexedStringProtocol) -> bool:
        return all((tester(indexed_string) for tester in self.testers))


def is_numeric(indexed_string: IndexedStringProtocol) -> bool:
    """String can be a number."""
    return indexed_string.txt.isnumeric()


def is_whitespace(indexed_string: IndexedStringProtocol) -> bool:
    """String contains only white space"""
    return indexed_string.txt.isspace()


def not_white_space(indexed_string: IndexedStringProtocol) -> bool:
    """String does not contain only white space."""
    return not is_whitespace(indexed_string)


def pass_through(indexed_string: IndexedStringProtocol) -> bool:
    """True for all strings."""
    _ = indexed_string
    return True
