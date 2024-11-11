from pathlib import Path
from typing import Sequence

from pbs_parse.snippets.indexed_string.index_strings import index_strings
from pbs_parse.snippets.indexed_string.state_parser import parsers
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext
from pbs_parse.snippets.indexed_string.state_parser.parse_scheme import ParseScheme
from pbs_parse.snippets.indexed_string.state_parser.protocols import (
    IndexedStringParserProtocol,
)
from pbs_parse.snippets.indexed_string.state_parser.result_handler import (
    SaveResultsToFile,
)
from pbs_parse.snippets.indexed_string.state_parser.state_parser import StateParser

DATA = """

There are five tokens here
one line



two: lines foo three: values bar bat
123 22323 3455
three lines of text
"""
scheme: dict[str, Sequence[IndexedStringParserProtocol]] = {
    "start": [
        parsers.SkipWhiteSpace(),
        parsers.NumberOfTokens(state="three_tokens", token_count=3),
        parsers.NumberOfTokens(state="five_tokens", token_count=5),
    ],
    "three_tokens": [],
    "five_tokens": [
        parsers.SkipWhiteSpace(),
        parsers.NumberOfTokens(state="two_tokens", token_count=2),
    ],
    "two_tokens": [parsers.SkipWhiteSpace(), parsers.KeyValue(state="key_value")],
    "key_value": [
        parsers.NumberOfTokens(state="five_tokens", token_count=5),
        parsers.OnlyNumbers(state="only_numbers"),
    ],
    "only_numbers": [parsers.OnlyAlphas(state="only_alphas")],
    "only_alphas": [parsers.SkipWhiteSpace()],
}


def test_parse(test_output_dir: Path):
    path_out = test_output_dir / "state_parser" / "parse_one" / "results.json"
    result_handler = SaveResultsToFile(path_out=path_out, overwrite=False)
    parse_scheme = ParseScheme(beginning_state="start", parser_lookup=scheme)
    parser = StateParser(parse_scheme=parse_scheme, result_handler=result_handler)
    string_factory = index_strings(strings=DATA.split("\n"), index_start=1)
    ctx = ParseContext(beginning_state=parse_scheme.beginning_state)
    parser.parse(ctx=ctx, data=string_factory)

    print(f"{len(result_handler.results.results)}")
    assert len(result_handler.results.results) == 11
