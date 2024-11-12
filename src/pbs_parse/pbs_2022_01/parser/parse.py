from pathlib import Path
from typing import Optional

from pbs_parse.pbs_2022_01.parser.parse_table import parse_table
from pbs_parse.snippets.indexed_string.model import IndexedStrings
from pbs_parse.snippets.indexed_string.state_parser.model import ParsedIndexedStrings
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from pbs_parse.snippets.indexed_string.state_parser.parse_exception import (
    ParseException,
)
from pbs_parse.snippets.indexed_string.state_parser.parse_scheme import ParseScheme
from pbs_parse.snippets.indexed_string.state_parser.protocols import ParseSchemeProtocol
from pbs_parse.snippets.indexed_string.state_parser.result_handler import CollectResults
from pbs_parse.snippets.indexed_string.state_parser.state_parser import StateParser


class TripParser:
    def __init__(self, scheme: Optional[ParseSchemeProtocol] = None) -> None:
        if scheme is None:
            scheme = ParseScheme(parser_lookup=parse_table())
        self.scheme = scheme

    def parse_file(self, ctx: ParseContext, path_in: Path) -> ParsedIndexedStrings:
        data = IndexedStrings.from_file(file_path=path_in)
        handler = CollectResults()
        parser = StateParser(parse_scheme=self.scheme, result_handler=handler)
        try:
            parser.parse(ctx=ctx, data=data.strings)
        except ParseException as e:
            print(e)
        return handler.results.data()
