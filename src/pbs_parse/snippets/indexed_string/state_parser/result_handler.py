from pathlib import Path
from types import TracebackType
from typing import Optional, Type

from pbs_parse.snippets.indexed_string.state_parser.model import ParseResults
from pbs_parse.snippets.indexed_string.state_parser.protocols import (
    ParseContextProtocol,
    ParseResultProtocol,
)


class SaveResultsToFile:
    """Do something with a parse result.

    Use as a context manager allows setup and trear down of assets if needed.
    """

    def __init__(self, path_out: Path, overwrite: bool = False) -> None:
        self.path_out = path_out
        self.results: ParseResults = ParseResults()
        self.overwrite = overwrite

    def __enter__(self) -> None: ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self.results.to_file(path_out=self.path_out, overwrite=self.overwrite)

    def handle_result(
        self,
        ctx: ParseContextProtocol,
        parse_result: ParseResultProtocol,
    ) -> None:
        """
        Handle the result of a successful parse.

        Args:
            parse_result: The result of a successful parse.
        """
        self.results.results.append(parse_result)
