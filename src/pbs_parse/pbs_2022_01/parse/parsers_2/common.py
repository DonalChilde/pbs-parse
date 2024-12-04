# ruff: noqa: D100 D101 D107 D102

import logging
from typing import Any

import pyparsing as pp
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser.abc import ParseContextABC, ParserABC
from pfmsoft.state_parser.model import ParsedIndexedString, ParseResult
from pfmsoft.state_parser.parse_exception import SingleParserFail

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PyparsingParserABC(ParserABC):
    """Base class for pyparsing parsers."""

    def __init__(self, state: str) -> None:
        super().__init__(state)

    def get_parsed_data(
        self, indexed_string: IndexedString, string_parser: pp.ParserElement
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
                parser_name=self.__class__.__name__,
                indexed_string=indexed_string,
            ) from error
        return result

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        raise NotImplementedError


class SimplePyparsingParser(PyparsingParserABC):
    """This parser assumes that the parsed data has been cleaned.

    The parse grammar has a parse action that cleans the parsed data.
    """

    def __init__(self, state: str, string_parser: pp.ParserElement) -> None:
        super().__init__(state)
        self.string_parser = string_parser

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        parse_result = self.get_parsed_data(
            indexed_string=input, string_parser=self.string_parser
        )
        data: dict[str, Any] = parse_result[0]  # type: ignore
        return ParseResult(
            current_state=self.state,
            parsed_indexed_string=ParsedIndexedString(
                id=self.state, indexed_string=input, data=data
            ),
        )
