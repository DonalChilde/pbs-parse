from typing import Sequence

from pbs_parse.snippets.indexed_string.state_parser.parse_exception import ParseJobFail
from pbs_parse.snippets.indexed_string.state_parser.protocols import (
    IndexedStringParserProtocol,
)


class ParseScheme:
    def __init__(
        self,
        beginning_state: str,
        parser_lookup: dict[str, Sequence[IndexedStringParserProtocol]],
    ) -> None:
        self.beginning_state = beginning_state
        self.parser_lookup = parser_lookup

    def next_parsers(self, key: str) -> Sequence[IndexedStringParserProtocol]:
        """Return a sequence of parsers based on a key.

        The key typically represents the current state of the parser, and the
        sequence of parsers are the expected matches for the next IndexedString.
        """
        parsers = self.parser_lookup.get(key, None)
        if parsers is None:
            raise ParseJobFail(f"Failed to find parsers using key: {key}")
        return parsers
