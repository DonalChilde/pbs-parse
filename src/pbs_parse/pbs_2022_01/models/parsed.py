from dataclasses import dataclass

from pbs_parse.snippets.indexed_string.state_parser.model import ParsedIndexedString


@dataclass
class ParsedTrip:
    uuid: str
    source: str
    parsed_lines: list[ParsedIndexedString]
