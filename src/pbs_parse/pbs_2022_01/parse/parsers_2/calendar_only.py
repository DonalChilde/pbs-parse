# ruff: noqa: D100 D101 D107 D102
import logging

from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser.abc import ParseContextABC
from pfmsoft.state_parser.model import ParsedIndexedString, ParseResult
from pfmsoft.state_parser.parse_exception import SingleParserFail

from pbs_parse.pbs_2022_01.parse import grammar_2 as G
from pbs_parse.snippets.strings.get_leading_whitespace import get_leading_whitespace

from .common import PyparsingParser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CalendarOnly(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = G.calendar_only

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        expected_len = 20
        ws_len = len(get_leading_whitespace(input.txt))
        if ws_len < expected_len:
            raise SingleParserFail(
                f"Expected at least {expected_len} leading whitespace characters, got {ws_len}",
                parser_name=self.__class__.__name__,
                indexed_string=input,
            )
        data = self.get_parsed_data(indexed_string=input)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)
