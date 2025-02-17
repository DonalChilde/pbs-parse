"""FILE: test_parse_one.py."""

import logging
from collections.abc import Sequence
from pathlib import Path

from pbs_parse.snippets.indexed_string import index_strings

# from pfmsoft.indexed_string.index_strings import index_strings
# from pfmsoft.state_parser import parsers
# from pfmsoft.state_parser.abc import ParserABC
# from pfmsoft.state_parser.model import parse_result_serializer
# from pfmsoft.state_parser.result_handler import (
#     SaveResultsToFile,
# )
# from pfmsoft.state_parser import (
#     StateParser,
#     ParseContext,
#     ParseScheme,
# )
from pbs_parse.snippets.indexed_string_state_parser import (
    ParseContext,
    ParseScheme,
    parse,
    parsers,
    result_handlers,
)
from pbs_parse.snippets.indexed_string_state_parser import protocol as P

logger = logging.getLogger(__name__)
DATA = """

There are five tokens here
one line



two: lines foo three: values bar bat
123 22323 3455
three lines of text
"""
scheme: dict[str, Sequence[P.Parser]] = {
    "start": [
        parsers.SkipWhiteSpace(),
        parsers.NumberOfTokens(parsed_state="three_tokens", token_count=3),
        parsers.NumberOfTokens(parsed_state="five_tokens", token_count=5),
    ],
    "three_tokens": [],
    "five_tokens": [
        parsers.SkipWhiteSpace(),
        parsers.NumberOfTokens(parsed_state="two_tokens", token_count=2),
    ],
    "two_tokens": [
        parsers.SkipWhiteSpace(),
        parsers.KeyValue(parsed_state="key_value"),
    ],
    "key_value": [
        parsers.NumberOfTokens(parsed_state="five_tokens", token_count=5),
        parsers.OnlyNumbers(parsed_state="only_numbers"),
    ],
    "only_numbers": [parsers.OnlyAlphas(parsed_state="only_alphas")],
    "only_alphas": [parsers.SkipWhiteSpace()],
}


def test_parse(test_output_dir: Path):  # noqa: D103
    path_out = (
        test_output_dir / "state_parser" / "parse_one" / "test_parse" / "results.json"
    )
    result_handler = result_handlers.SaveResultsToFile(
        path_out=path_out, overwrite=False
    )
    parse_scheme = ParseScheme(parser_lookup=scheme)
    # parser = StateParser(parse_scheme=parse_scheme, result_handler=result_handler)
    string_factory = index_strings(strings=DATA.split("\n"), index_start=1)
    ctx = ParseContext()
    parse(
        ctx=ctx,
        data=string_factory,
        parse_scheme=parse_scheme,
        result_handler=result_handler,
    )
    print(f"{len(result_handler.results)}")
    assert len(result_handler.results) == 11


def test_serializer_parse_results(test_output_dir: Path):  # noqa: D103
    path_out = (
        test_output_dir
        / "state_parser"
        / "parse_one"
        / "test_serializer"
        / "results.json"
    )
    result_handler = result_handlers.SaveResultsToFile(
        path_out=path_out, overwrite=False
    )
    parse_scheme = ParseScheme(parser_lookup=scheme)
    # parser = StateParser(parse_scheme=parse_scheme, result_handler=result_handler)
    string_factory = index_strings(strings=DATA.split("\n"), index_start=1)
    ctx = ParseContext()
    parse(
        ctx=ctx,
        data=string_factory,
        parse_scheme=parse_scheme,
        result_handler=result_handler,
    )
    result = result_handler.results
    print(f"{len(result)}")
    assert len(result) == 11
    # serializer = parse_result_serializer()
    # loaded_results = serializer.load_from_json_list(path_in=path_out)
    # path_out_loaded = (
    #     test_output_dir / "state_parser" / "parse_one" / "results_loaded.json"
    # )
    # serializer.save_iter_as_json(path_out=path_out_loaded, complex_obj=loaded_results)
    # logger.info(f"       results:{result!r}")
    # logger.info(f"loaded_results:{loaded_results!r}")
    # assert loaded_results.__repr__() == result.__repr__()
