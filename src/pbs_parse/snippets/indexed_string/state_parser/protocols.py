"""
Defines the interface for a state based indexed string parser.

When parsing semi structured text, parsing a section often depends on
knowing what the previous section was. This parser allows the selection of possible
parsers based on the results of the previous successfully parsed string.
"""

from types import TracebackType
from typing import Iterable, Optional, Protocol, Sequence, Type

from pbs_parse.snippets.indexed_string.protocols import IndexedStringProtocol


class ParsedIndexedStringProtocol(Protocol):
    id: str
    indexed_string: IndexedStringProtocol
    data: dict[str, str]


class ParseResultProtocol(Protocol):
    current_state: str
    result: ParsedIndexedStringProtocol


class ParseContextProtocol(Protocol):
    current_state: str = ""


class IndexedStringParserProtocol(Protocol):
    """Parse an IndexedString."""

    def parse(
        self, ctx: ParseContextProtocol, data: IndexedStringProtocol
    ) -> ParseResultProtocol:
        """
        A parse function that matches an IndexedString.

        Raise ParseFail on a parse error. Pass any additional information
        required in the ctx. A successful parse also determines the new state of the
        parse job.

        Args:
            indexed_string: The indexed string to be parsed.
            ctx: A dictionary that holds any additional information needed for parsing.

        Raises:
            ParseFail: Raises a ParseFail exception for a failed parse.
            ParseAllFail: Raised to kill a parse job from inside an indiviual parser.

        Returns:
            The `ParseResult` of a successful parse.
        """
        ...


class ResultHandlerProtocol(Protocol):
    """Do something with a parse result.

    Use as a context manager allows setup and trear down of assets if needed.
    """

    def __enter__(self) -> None: ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]: ...

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
        ...


class ParseSchemeProtocol(Protocol):
    beginning_state: str

    def next_parsers(self, key: str) -> Sequence[IndexedStringParserProtocol]:
        """Return a sequence of parsers based on a key.

        The key typically represents the current state of the parser, and the
        sequence of parsers are the expected matches for the next IndexedString.
        """
        ...


class StateParserProtocol(Protocol):
    parse_scheme: ParseSchemeProtocol
    result_handler: ResultHandlerProtocol

    def parse(
        self, ctx: ParseContextProtocol, data: Iterable[IndexedStringProtocol]
    ) -> None: ...
