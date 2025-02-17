# ruff: noqa: D100 D101 D107 D102

import logging
from typing import Any

import pyparsing as pp

from pbs_parse.snippets.indexed_string import IndexedStringProtocol
from pbs_parse.snippets.indexed_string_state_parser import protocol as P
from pbs_parse.snippets.indexed_string_state_parser.exceptions import SingleParserFail
from pbs_parse.snippets.indexed_string_state_parser.model import (
    ParsedIndexedString,
    ParseResult,
)
from pbs_parse.snippets.indexed_string_state_parser.parsers import ParserABC

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PyparsingParserABC(ParserABC):
    """Base class for pyparsing parsers."""

    def __init__(self, parsed_state: str) -> None:
        super().__init__(parsed_state=parsed_state)

    def get_parsed_data(
        self,
        ctx: P.ParseContext,
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
                f"{error}", parser=self, indexed_string=indexed_string, ctx=ctx
            ) from error
        return result

    def parse(self, ctx: P.ParseContext, input: IndexedStringProtocol) -> ParseResult:
        raise NotImplementedError


class SimplePyparsingParser(PyparsingParserABC):
    """This parser assumes that the parsed data has been cleaned.

    The parse grammar has a parse action that cleans the parsed data.
    """

    def __init__(self, parsed_state: str, string_parser: pp.ParserElement) -> None:
        super().__init__(parsed_state=parsed_state)
        self.string_parser = string_parser

    def parse(self, ctx: P.ParseContext, input: IndexedStringProtocol) -> ParseResult:
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
