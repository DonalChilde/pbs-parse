# ruff: noqa: D100 D101 D107 D102

import logging
from abc import ABC, abstractmethod
from typing import Any

import pyparsing as pp

from pbs_parse.snippets.indexed_string import IndexedStringProtocol
from pbs_parse.snippets.indexed_string.pydantic_model import IndexedString
from pbs_parse.snippets.indexed_string_state_parser import ParseContext
from pbs_parse.snippets.indexed_string_state_parser.exceptions import SingleParserFail
from pbs_parse.snippets.indexed_string_state_parser.pydantic_model import (
    ParsedIndexedString,
    ParseResult,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ParserABC(ABC):
    """ParserABC.

    Args:
        parsed_state (str): The state that is returned as part of the ParseResult
            after a successful parse.
    """

    def __init__(self, parsed_state: str) -> None:
        """__init__.

        Args:
            parsed_state (str): The state that is returned as part of the ParseResult
                after a successful parse.
        """
        super().__init__()
        self.parsed_state = parsed_state

    @abstractmethod
    def parse(self, ctx: ParseContext, input: IndexedString) -> ParseResult:
        """Parse an IndexedString.

        Args:
            ctx (P.ParseContext): _description_
            input (IndexedStringProtocol): _description_

        Raises:
            NotImplementedError: _description_

        Returns:
            P.ParseResult: _description_
        """
        raise NotImplementedError

    def parse_fail(self, msg: str, ctx: ParseContext, input: IndexedString):
        """parse_fail.

        A convenience method for signaling the failure or this parser to match the input.

        Args:
            msg (str): _description_
            ctx (P.ParseContext): _description_
            input (IndexedStringProtocol): _description_


        Raises:
            SingleParserFail: _description_
        """
        raise SingleParserFail(msg=msg, parser=self, indexed_string=input, ctx=ctx)  # type: ignore

    def __repr__(self) -> str:
        """Repr."""
        return f"ParserABC(parsed_state={self.parsed_state})"


class PyparsingParserABC(ParserABC):
    """Base class for pyparsing parsers."""

    def __init__(self, parsed_state: str) -> None:
        super().__init__(parsed_state=parsed_state)

    def get_parsed_data(
        self,
        ctx: ParseContext,
        indexed_string: IndexedStringProtocol,
        string_parser: pp.ParserElement,
    ) -> pp.ParseResults:
        """Attempt to parse a string.

        SingleParserFail indicates that this parser failed, but not necessarily the
        whole job.

        """
        try:
            result = string_parser.parse_string(indexed_string.txt)
        except pp.ParseException as error:
            raise SingleParserFail(
                f"{error}",
                parser=self,  # type: ignore
                indexed_string=indexed_string,
                ctx=ctx,
            ) from error
        return result

    @abstractmethod
    def parse(self, ctx: ParseContext, input: IndexedString) -> ParseResult:
        raise NotImplementedError


class SimplePyparsingParser(PyparsingParserABC):
    """This parser assumes that the parsed data has been cleaned.

    The parse grammar has a parse action that cleans the parsed data.
    """

    def __init__(self, parsed_state: str, string_parser: pp.ParserElement) -> None:
        super().__init__(parsed_state=parsed_state)
        self.string_parser = string_parser

    def parse(self, ctx: ParseContext, input: IndexedString) -> ParseResult:
        _ = ctx
        parse_result = self.get_parsed_data(
            ctx=ctx, indexed_string=input, string_parser=self.string_parser
        )
        data: dict[str, Any] = parse_result[0]  # type: ignore
        return ParseResult(
            parsed_state=self.parsed_state,
            parsed_indexed_string=ParsedIndexedString(
                id=self.parsed_state, indexed_string=input, data=data
            ),
        )

    def __repr__(self) -> str:
        """Repr."""
        return f"SimplePyparsingParser(parsed_state={self.parsed_state}, string_parser={self.string_parser})"
