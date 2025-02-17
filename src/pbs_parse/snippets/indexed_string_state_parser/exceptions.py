"""FILE: parse_exception.py."""

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
from collections.abc import Sequence

from . import IndexedStringProtocol
from . import protocol as P


class ParseException(Exception):
    """Base Exception for ParseExceptions."""


class SingleParserFail(ParseException):
    """Use this exception to signal a single parser failed."""

    def __init__(
        self,
        msg: str,
        parser: P.Parser,
        indexed_string: IndexedStringProtocol,
        ctx: P.ParseContext,
        *args: object,
    ) -> None:
        """__init__.

        Args:
            msg (str): _description_
            parser (P.Parser): _description_
            indexed_string (IndexedStringProtocol): _description_
            ctx (P.ParseContext): _description_
            *args (object): _description_
        """
        super().__init__(msg, *args)
        self.parser = parser
        self.indexed_string = indexed_string
        self.ctx = ctx


class ParseJobFail(ParseException):
    """Use this exception to signal whole parse job failed.

    For failures other than all parsers failed to match.
    """

    def __init__(self, msg: str, *args: object) -> None:
        """__init__.

        Args:
            msg (str): _description_
            *args (object): _description_
        """
        super().__init__(msg, *args)


class ParseAllFail(ParseJobFail):
    """Use this exception to signal all parsers failed, job failed."""

    def __init__(
        self,
        msg: str,
        parsers: Sequence[P.Parser],
        indexed_string: IndexedStringProtocol,
        ctx: P.ParseContext,
        *args: object,
    ) -> None:
        """__init__.

        Args:
            msg (str): _description_
            parsers (Sequence[P.Parser]): _description_
            indexed_string (IndexedStringProtocol): _description_
            ctx (P.ParseContext): _description_
            *args (object): _description_
        """
        super().__init__(msg, *args)
        self.parsers = parsers
        self.indexed_string = indexed_string
        self.ctx = ctx


# class ParseValidationError(ParseException):
#     # TODO not sure of the place for this, validation more likely to take place
#     #   outside parser.
#     def __init__(self, *args: object) -> None:
#         super().__init__(*args)
