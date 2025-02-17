"""Protocol to define a state parser."""

from collections.abc import Sequence
from types import TracebackType
from typing import Any, Protocol, Self

from . import IndexedStringProtocol


class ParseContext(Protocol):
    """ParseContext is used to store values between each parse of an IndexedString.

    Normally a  new `ParseContext` will be created for each parse, as the current_state
    will normally have to be reset to a starting value.

    Args:
        current_state (str): The current state of the parse. This is used to select the
            parsers to try on the next IndexedString.
        obj (dict[str, Any]): Can be used to store arbitrary values for use during the parse.
    """

    current_state: str
    obj: dict[str, Any]


class ParsedIndexedString(Protocol):
    """ParsedIndexedString is data captured from a parse.

    Args:
        id (str): A value that can be used to later to identify and further process the
            parsed data. This can often be the parsed_state of the parser, but can be
            any string value.
        indexed_string (IndexedStringProtocol): The IndexedString that was parsed.
        data (dict[str, Any]): The data parsed from the IndexedString.
    """

    id: str
    indexed_string: IndexedStringProtocol
    data: dict[str, Any]


class ParseResult(Protocol):
    """ParseResult.

    The result returned from a Parser.

    Args:
        parsed_state (str): The state of the parse after the successful match. This value
        is expected to be used outside the Parser to update the ParseContext.current_state.
        parsed_indexed_string (ParsedIndexedString): The data captured from a parse.
    """

    parsed_state: str
    parsed_indexed_string: ParsedIndexedString


class ResultHandler(Protocol):
    """ResultHandler processes the results of a parse.

    This is expected to be a context manager because many of the actions that are expected
    to be taken with parsed data involve saving to a file, or other actions that would
    benefit from having resource management built in.

    """

    def __enter__(self) -> Self:
        """__enter__.

        Returns:
            Self: _description_
        """
        ...

    def __exit__(  # noqa: D105
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """__exit__.

        Args:
            exc_type (type[BaseException] | None): _description_
            exc_value (BaseException | None): _description_
            traceback (TracebackType | None): _description_

        Returns:
            bool | None: _description_
        """
        ...

    def handle_result(self, ctx: ParseContext, parse_result: ParseResult) -> None:
        """handle_result.

        Args:
            ctx (ParseContext): _description_
            parse_result (ParseResult): _description_
        """
        ...


class Parser(Protocol):
    """Parser.

    Args:
        parsed_state (str): The state of the parse after the successful match. This value
        is expected to be used outside the Parser to update the ParseContext.current_state.

    Raises:
        SingleParserFail: A failed parse should raise `SingelParserFail`.
    """

    parsed_state: str

    def parse(self, ctx: ParseContext, input: IndexedStringProtocol) -> ParseResult:
        """Attempt to parse the input.

        Args:
            ctx (ParseContext): _description_
            input (IndexedStringProtocol): _description_

        Raises:
        SingleParserFail: A failed parse should raise `SingelParserFail`.

        Returns:
            ParseResult: _description_
        """
        ...


class ParseScheme(Protocol):
    """ParseScheme.

    The look up source for the parsers expected to match the next IndexedString.
    """

    def next_parsers(self, key: str) -> Sequence[Parser]:
        """next_parsers.

        Return the list of parsers expected to match the next IndexedString.

        Args:
            key (str): The key to lookup the parsers expected to match the next IndexedString.
                This is normally the `ctx.current_state` value.

        Returns:
            Sequence[Parser]: _description_
        """
        ...


# class StateParser(Protocol):
#     parse_scheme: ParseScheme
#     result_handler: ResultHandler

#     def parse(
#         self, ctx: ParseContext, data: Iterable[IndexedStringProtocol]
#     ) -> None: ...
