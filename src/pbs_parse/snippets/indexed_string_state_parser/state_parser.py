"""FILE: state_parser_2.py."""

import logging
from collections.abc import Iterable, Sequence
from typing import Any

from . import (
    IndexedString,
    IndexedStringProtocol,
)
from . import protocol as P
from .exceptions import (
    ParseAllFail,
    ParseException,
    ParseJobFail,
    SingleParserFail,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ParseContext:
    """ParseContext is used to store values between each parse of an IndexedString.

    Normally a  new `ParseContext` will be created for each parse, as the current_state
    will normally have to be reset to a starting value.

    Args:
        current_state (str): The current state of the parse. This is used to select the
            parsers to try on the next IndexedString.
        obj (dict[str, Any]): Can be used to store arbitrary values for use during the parse.
    """

    def __init__(
        self, current_state: str = "start", obj: dict[str, Any] | None = None
    ) -> None:
        """__init_.

        Args:
            current_state (str, optional): _description_. Defaults to "start".
            obj (dict[str, Any] | None, optional): _description_. Defaults to None.
        """
        self.current_state = current_state
        if obj is None:
            self.obj: dict[str, Any] = {}
        else:
            self.obj = obj


class ParseScheme:
    """ParseScheme.

    The look up source for the parsers expected to match the next IndexedString.
    """

    def __init__(
        self,
        parser_lookup: dict[str, Sequence[P.Parser]],
    ) -> None:
        """__init__.

        Args:
            parser_lookup (dict[str, Sequence[P.Parser]]): _description_
        """
        self.parser_lookup = parser_lookup

    def next_parsers(self, key: str) -> Sequence[P.Parser]:
        """Return a sequence of parsers based on a key.

        The key typically represents the current state of the parser, and the
        sequence of parsers are the expected matches for the next IndexedString.

        Args:
            key (str): The key to lookup the parsers expected to match the next IndexedString.
                This is normally the `ctx.current_state` value.
        """
        parsers = self.parser_lookup.get(key, None)
        if parsers is None:
            raise ParseJobFail(f"Failed to find parsers using key: {key}")
        return parsers


def parse(
    ctx: P.ParseContext,
    data: Iterable[IndexedString],
    parse_scheme: P.ParseScheme,
    result_handler: P.ResultHandler,
) -> None:
    """Parse an iterable of indexed strings.

    Parses an iterable of indexed strings, eg. (idx=linenumber, txt=line).
    Uses `ctx.current_state` to store the state of the parse, which is used to predict
    the possible matches for the next indexed string.

    The beginning state is defined by the parse scheme, and each successful parse
    will advance the state. This new state will be used to get a list of possible
    parsers from the parse scheme, which will be checked in sequence until a match
    is found. If no valid matches are found, a `ParseAllFail` will be raised,
    signaling a failure of the parse job. In other words, a match must be found for
    each `IndexedString`.

    Args:
        ctx (P.ParseContext): _description_
        data (Iterable[IndexedString]): _description_
        parse_scheme (P.ParseScheme): _description_
        result_handler (P.ResultHandler): _description_

    Raises:
        ParseJobFail: Signals the failure of the parse job as a whole for reasons other
            than the parsers not matching.
        ParseAllFail: Signals the failure of all parsers to match, and thus the parse
            job as a whole.
    """
    with result_handler as handler:
        for parse_result in parse_indexed_strings(
            ctx=ctx, data=data, parse_scheme=parse_scheme
        ):
            handler.handle_result(ctx=ctx, parse_result=parse_result)


def parse_indexed_strings(
    ctx: P.ParseContext,
    data: Iterable[IndexedStringProtocol],
    parse_scheme: P.ParseScheme,
) -> Iterable[P.ParseResult]:
    """parse_indexed_strings.

    Args:
        ctx (P.ParseContext): Stores extra information needed complete the parse.
        data (Iterable[IndexedStringProtocol]): _description_
        parse_scheme (P.ParseScheme): _description_

    Raises:
        ParseJobFail: Signals the failure of the parse job as a whole for reasons other
            than the parsers not matching.
        ParseAllFail: Signals the failure of all parsers to match, and thus the parse
            job as a whole.

    Returns:
        Iterable[P.ParseResult]: _description_

    Yields:
        Iterator[Iterable[P.ParseResult]]: _description_
    """
    made_an_attempt: bool = False
    for indexed_string in data:
        made_an_attempt = True
        try:
            parse_result = parse_indexed_string(
                indexed_string=indexed_string,
                parsers=parse_scheme.next_parsers(key=ctx.current_state),
                ctx=ctx,
            )
            yield parse_result
        except ParseAllFail as error:
            # All the provided parsers failed to match.
            logger.error("%s", error)
            raise error
        except ParseJobFail as error:
            # This is started from individual parser
            logger.error(
                "Parse Job failed: %s Current State:%r IndexedString:%r",
                error,
                ctx.current_state,
                indexed_string,
            )
            raise error
        except ParseException as error:
            # unexpected exception
            logger.error("%s", error)
            raise error
    if not made_an_attempt:
        failed_attempt = ParseJobFail(
            "No IndexedStrings provided to this parse attempt."
        )
        logger.error("%s", failed_attempt)
        raise failed_attempt


def parse_indexed_string(
    indexed_string: IndexedStringProtocol,
    parsers: Sequence[P.Parser],
    ctx: P.ParseContext,
) -> P.ParseResult:
    """Parse an indexed string based on a list of possible parsers.

    The failure of an individual parser should raise a `ParseException`. This does not
    represent a failure of the parse job as a whole, unless none of the parsers
    successfully match.

    Args:
        indexed_string (IndexedStringProtocol): An indexed string to parse.
        parsers (Sequence[P.Parser]): A sequence of parsers to try.
        ctx (P.ParseContext): Stores extra information needed complete the parse.

    Raises:
        ParseJobFail: Signals the failure of the parse job as a whole for reasons other
            than the parsers not matching.
        ParseAllFail: Signals the failure of all parsers to match, and thus the parse
            job as a whole.

    Returns:
        P.ParseResult: The result of a successful parse.
    """
    for parser in parsers:
        try:
            parse_result = parser.parse(input=indexed_string, ctx=ctx)
            ctx.current_state = parse_result.parsed_state
            return parse_result
        except SingleParserFail as error:
            # log and continue to try next parser.
            logger.debug("%s", error)
        except Exception as error:
            raise ParseJobFail(
                msg=f"There was an exception during parsing. {error!r}",
            ) from error
    error = ParseAllFail(
        msg="No successful parser found for indexed_string.",
        indexed_string=indexed_string,
        parsers=parsers,
        ctx=ctx,
    )
    raise error
