# ruff: noqa: D100 D101 D107 D102

import logging
from typing import Any

import pyparsing as pp
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser.abc import ParseContextABC, ParserABC
from pfmsoft.state_parser.model import ParseResult
from pfmsoft.state_parser.parse_exception import SingleParserFail

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PyparsingParser(ParserABC):
    """Base class for pyparsing parsers."""

    def __init__(self, state: str) -> None:
        super().__init__(state)

    p_parser: pp.ParserElement

    def get_parsed_data(self, indexed_string: IndexedString) -> dict[str, Any]:
        """Attempt to parse a string.

        SingleParserFail indicates that this parser failed, but not necessarily the
        whole job.

        result[0] assumes that the data was cleaned in a parse action during parsing.
        """
        try:
            result = self.p_parser.parse_string(indexed_string.txt)
        except pp.ParseException as error:
            raise SingleParserFail(
                f"{error}",
                parser_name=self.__class__.__name__,
                indexed_string=indexed_string,
            ) from error
        return result[0]  # type: ignore

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        raise NotImplementedError
