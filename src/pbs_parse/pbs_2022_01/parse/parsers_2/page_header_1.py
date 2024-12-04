"""Parser for page header 1."""

import logging

from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser.abc import ParseContextABC, ParserABC
from pfmsoft.state_parser.model import ParsedIndexedString, ParseResult
from pfmsoft.state_parser.parse_exception import SingleParserFail

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PageHeader1(ParserABC):
    """Parser for page header 1."""

    def __init__(self, state: str) -> None:
        """_summary_.

        Args:
            state (str): new state if parse successful.
        """
        super().__init__(state)

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        """Parse."""
        _ = ctx
        if "DEPARTURE" in input.txt:
            result = ParsedIndexedString(id=self.state, indexed_string=input, data={})
            return ParseResult(current_state=self.state, parsed_indexed_string=result)

        raise SingleParserFail(
            f"'DEPARTURE' not found in {input!r}.",
            parser_name=self.__class__.__name__,
            indexed_string=input,
        )
