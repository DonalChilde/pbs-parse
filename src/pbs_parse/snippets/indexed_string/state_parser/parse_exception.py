####################################################
#                                                  #
#  src/snippets/indexed_string/state_parser/parse_exception.py
#                                                  #
####################################################
# Created by: Chad Lowe                            #
# Created on: 2023-02-05T05:59:31-07:00            #
# Last Modified: 2023-04-22T15:59:58.363420+00:00  #
# Source: https://github.com/DonalChilde/snippets  #
####################################################
from typing import Sequence

from pbs_parse.snippets.indexed_string.protocols import IndexedStringProtocol
from pbs_parse.snippets.indexed_string.state_parser.protocols import (
    IndexedStringParserProtocol,
)


class ParseException(Exception):
    """Use this exception to signal a failed parse."""


class SingleParserFail(ParseException):
    """Use this exception to signal single parser failed."""

    def __init__(
        self,
        msg: str,
        parser: IndexedStringParserProtocol,
        indexed_string: IndexedStringProtocol,
        *args: object,
    ) -> None:
        super().__init__(msg, *args)
        self.parser = parser
        self.indexed_string = indexed_string


class ParseJobFail(ParseException):
    """Use this exception to signal whole parse job failed."""

    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(msg, *args)


class ParseAllFail(ParseJobFail):
    """Use this exception to signal all parsers failed, job failed."""

    def __init__(
        self,
        msg: str,
        parsers: Sequence[IndexedStringParserProtocol],
        indexed_string: IndexedStringProtocol,
        *args: object,
    ) -> None:
        super().__init__(msg, *args)
        self.parsers = parsers
        self.indexed_string = indexed_string


class ParseValidationError(ParseException):
    # TODO not sure of the place for this, validation more likely to take place
    #   outside parser.
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
