# ruff: noqa: D100 D101 D107 D102
import logging

from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser.abc import ParseContextABC
from pfmsoft.state_parser.model import ParsedIndexedString, ParseResult

from pbs_parse.pbs_2022_01.parse import grammar_2 as G

from .common import PyparsingParser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class BaseEquipment(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = G.base_equipment

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        data = self.get_parsed_data(indexed_string=input)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)
