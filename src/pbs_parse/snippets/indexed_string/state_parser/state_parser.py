import logging
from typing import Iterable, Sequence

from pbs_parse.snippets.indexed_string.protocols import IndexedStringProtocol
from pbs_parse.snippets.indexed_string.state_parser.parse_exception import (
    ParseAllFail,
    ParseException,
    ParseJobFail,
    SingleParserFail,
)
from pbs_parse.snippets.indexed_string.state_parser.protocols import (
    IndexedStringParserProtocol,
    ParseContextProtocol,
    ParseResultProtocol,
    ParseSchemeProtocol,
    ResultHandlerProtocol,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class StateParser:
    def __init__(
        self, parse_scheme: ParseSchemeProtocol, result_handler: ResultHandlerProtocol
    ) -> None:
        self.result_handler = result_handler
        self.parse_scheme = parse_scheme

    def parse(
        self, ctx: ParseContextProtocol, data: Iterable[IndexedStringProtocol]
    ) -> None:
        """
        Parse an iterable of indexed strings.

        Parses an iterable of indexed strings, eg. (idx=linenumber, txt=line).
        Uses `state` to predict the possible matches for the next indexed string.
        The beginning state is defined by the parse scheme, and each successful parse
        will return a new state. This new state will be used to get a list of possible
        parsers from the parse scheme, which will be checked in sequence until a match
        is found. If no valid matches are found, a `ParseException` will be raised,
        signaling a failure of the parse job. In other words, a match must be found for
        each `IndexedString`.

        Args:
            ctx: A container for custom in formation that is passed to parsers.
            data: An iterable of indexed strings to be parsed.

        Raises:
            error: Signals a failure of the overall parse job.
        """
        with self.result_handler as handler:
            for result in self._parse_indexed_strings(ctx=ctx, data=data):
                handler.handle_result(ctx=ctx, parse_result=result)

    def _parse_indexed_strings(
        self, ctx: ParseContextProtocol, data: Iterable[IndexedStringProtocol]
    ) -> Iterable[ParseResultProtocol]:
        current_state = self.parse_scheme.beginning_state
        made_an_attempt: bool = False
        for indexed_string in data:
            made_an_attempt = True
            try:
                parse_result = self._parse_indexed_string(
                    indexed_string=indexed_string,
                    parsers=self.parse_scheme.next_parsers(key=current_state),
                    ctx=ctx,
                )
                current_state = parse_result.current_state
                yield parse_result
            except ParseAllFail as error:
                # All the provided parsers failed to match.
                logger.error("%s", error)
                raise error
            except ParseJobFail as error:
                # This is started from individual parser
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

    def _parse_indexed_string(
        self,
        indexed_string: IndexedStringProtocol,
        parsers: Sequence[IndexedStringParserProtocol],
        ctx: ParseContextProtocol,
    ) -> ParseResultProtocol:
        """
        Parse an indexed string based on a list of possible parsers.

        The failure of an individual parser should raise a `ParseException`. This does not
        represent a failure of the parse job as a whole, unless none of the parsers
        successfully match.

        Args:
            indexed_string: An indexed string to parse.
            parsers: A sequence of parsers to try.
            ctx: A store for arbitrary information needed to parse.

        Raises:
            SingleParserFail: Signals the failure of a parser.
            ParseJobFail: Signals the failure of the parse job as a whole.
            ParseAllFail: Signals the failure of all parsers.

        Returns:
            The result of a successful parse.
        """
        for parser in parsers:
            try:
                parse_result = parser.parse(input=indexed_string, ctx=ctx)
                ctx.current_state = parse_result.current_state
                return parse_result
            except SingleParserFail as error:
                logger.debug(
                    "\n\tFAILED %r->%r\n\t%r\n\tCurrent State:%r",
                    error.parser.__class__.__name__,
                    error.indexed_string,
                    error,
                    ctx.current_state,
                )
            except ParseJobFail as error:
                logger.error(
                    "Parse Job failed %s Current State:%r", error, ctx.current_state
                )
                raise error
        raise ParseAllFail(
            f"No parser found for \n\tindexed_string={indexed_string!r}"
            f"\n\tTried {parsers!r}\n\tCurrent State:{ctx.current_state}",
            parsers=parsers,
            indexed_string=indexed_string,
        )
