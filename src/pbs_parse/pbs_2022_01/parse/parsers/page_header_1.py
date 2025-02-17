"""Parser for page header 1."""

import logging

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


class PageHeader1(ParserABC):
    """Parser for page header 1."""

    def __init__(self, state: str) -> None:
        """_summary_.

        Args:
            state (str): new state if parse successful.
        """
        super().__init__(state)

    def parse(self, ctx: P.ParseContext, input: IndexedStringProtocol) -> P.ParseResult:
        """Parse."""
        _ = ctx
        if "DEPARTURE" in input.txt:
            result = ParsedIndexedString(
                id=self.parsed_state, indexed_string=input, data={}
            )
            return ParseResult(
                parsed_state=self.parsed_state, parsed_indexed_string=result
            )

        raise SingleParserFail(
            f"'DEPARTURE' not found in {input!r}.",
            parser=self,
            indexed_string=input,
            ctx=ctx,
        )
