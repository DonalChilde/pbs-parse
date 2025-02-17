"""Examples of parsers."""

from abc import ABC, abstractmethod

from . import IndexedStringProtocol
from . import protocol as P
from .exceptions import SingleParserFail
from .model import ParsedIndexedString, ParseResult


class ParserABC(ABC):
    """ParserABC.

    Args:
        parsed_state (str): The state that is returned as part of the ParseResult
            after a successful parse.
    """

    def __init__(self, parsed_state: str) -> None:
        """__init__.

        Args:
            parsed_state (str): The state that is returned as part of the ParseResult
                after a successful parse.
        """
        super().__init__()
        self.parsed_state = parsed_state

    @abstractmethod
    def parse(self, ctx: P.ParseContext, input: IndexedStringProtocol) -> P.ParseResult:
        """Parse an IndexedString.

        Args:
            ctx (P.ParseContext): _description_
            input (IndexedStringProtocol): _description_

        Raises:
            NotImplementedError: _description_

        Returns:
            P.ParseResult: _description_
        """
        raise NotImplementedError

    def parse_fail(self, msg: str, ctx: P.ParseContext, input: IndexedStringProtocol):
        """parse_fail.

        A convenience method for signaling the failure or this parser to match the input.

        Args:
            msg (str): _description_
            ctx (P.ParseContext): _description_
            input (IndexedStringProtocol): _description_


        Raises:
            SingleParserFail: _description_
        """
        raise SingleParserFail(msg=msg, parser=self, indexed_string=input, ctx=ctx)

    def __repr__(self) -> str:
        """Repr."""
        return f"ParserABC(parsed_state={self.parsed_state})"


class Tokenize(ParserABC):
    """Tokenize.

    Args:
        parsed_state (str): _description_
    """

    def __init__(self, parsed_state: str) -> None:
        """__init__.

        Args:
            parsed_state (str): _description_
        """
        super().__init__(parsed_state)

    def parse(self, ctx: P.ParseContext, input: IndexedStringProtocol) -> P.ParseResult:
        """Only fails on whitespace."""
        tokens = {"tokens": input.txt.split()}
        if not tokens["tokens"]:
            self.parse_fail(
                msg="No tokens found, is this whitespace only?", input=input, ctx=ctx
            )
        parsed = ParsedIndexedString(
            id=self.parsed_state, indexed_string=input, data=tokens
        )
        result = ParseResult(
            parsed_state=self.parsed_state, parsed_indexed_string=parsed
        )
        return result


class SkipWhiteSpace(ParserABC):
    """SkipWhiteSpace.

    Args:
        ParserABC (_type_): _description_
    """

    def __init__(self, parsed_state: str = "whitespace") -> None:
        """__init__.

        Args:
            parsed_state (str, optional): _description_. Defaults to "whitespace".
        """
        super().__init__(parsed_state)

    def parse(self, ctx: P.ParseContext, input: IndexedStringProtocol) -> P.ParseResult:
        """This parser fails if the input txt is not all whitespace.

        The parse state is not advanced, the parsed_state passed back is the
        ctx.current_state.
        """
        if input.txt.isspace():
            parsed = ParsedIndexedString(
                id=self.parsed_state, indexed_string=input, data={}
            )
            result = ParseResult(
                parsed_state=ctx.current_state, parsed_indexed_string=parsed
            )
            return result
        elif not input.txt:
            parsed = ParsedIndexedString(
                id=self.parsed_state, indexed_string=input, data={}
            )
            result = ParseResult(
                parsed_state=ctx.current_state, parsed_indexed_string=parsed
            )
            return result
        self.parse_fail(msg="This is not all whitespace", input=input, ctx=ctx)
        return result


class OnlyNumbers(ParserABC):
    """OnlyNumbers.

    Args:
        ParserABC (_type_): _description_
    """

    def __init__(self, parsed_state: str = "only_numbers") -> None:
        """__init__.

        Args:
            parsed_state (str, optional): _description_. Defaults to "only_numbers".
        """
        super().__init__(parsed_state)

    def parse(self, ctx: P.ParseContext, input: IndexedStringProtocol) -> P.ParseResult:
        """Only matches if input contains numbers with whitespace.

        Args:
            ctx (P.ParseContext): _description_
            input (IndexedStringProtocol): _description_

        Returns:
            P.ParseResult: _description_
        """
        tokens = input.txt.split()
        if not tokens:
            self.parse_fail(msg="This is all whitespace.", input=input, ctx=ctx)
        for item in tokens:
            if not item.isnumeric():
                self.parse_fail(msg="This is not all numbers.", input=input, ctx=ctx)
        parsed = ParsedIndexedString(
            id=self.parsed_state, indexed_string=input, data={"numbers": tokens}
        )
        result = ParseResult(
            parsed_state=self.parsed_state, parsed_indexed_string=parsed
        )
        return result


class OnlyAlphas(ParserABC):
    """OnlyAlphas.

    Args:
        ParserABC (_type_): _description_
    """

    def __init__(self, parsed_state: str = "alphas") -> None:
        """__init__.

        Args:
            parsed_state (str, optional): _description_. Defaults to "alphas".
        """
        super().__init__(parsed_state)

    def parse(self, ctx: P.ParseContext, input: IndexedStringProtocol) -> P.ParseResult:
        """Only matches when input is alpha charsacters plus white space.

        Args:
            ctx (P.ParseContext): _description_
            input (IndexedStringProtocol): _description_

        Returns:
            P.ParseResult: _description_
        """
        tokens = input.txt.split()
        if not tokens:
            self.parse_fail(msg="This is all whitespace.", input=input, ctx=ctx)
        for item in tokens:
            if not item.isalpha():
                self.parse_fail(msg="This is not all alphas.", input=input, ctx=ctx)
        parsed = ParsedIndexedString(
            id=self.parsed_state, indexed_string=input, data={"alphas": tokens}
        )
        result = ParseResult(
            parsed_state=self.parsed_state, parsed_indexed_string=parsed
        )
        return result


class KeyValue(ParserABC):
    """KeyValue.

    Args:
        ParserABC (_type_): _description_
    """

    def __init__(self, parsed_state: str) -> None:
        """__init__.

        Args:
            parsed_state (str): _description_
        """
        super().__init__(parsed_state)

    def parse(self, ctx: P.ParseContext, input: IndexedStringProtocol) -> P.ParseResult:
        """Only matches key:value tokens in input.

        This is a very limited matcher.

        Args:
            ctx (P.ParseContext): _description_
            input (IndexedStringProtocol): _description_

        Returns:
            P.ParseResult: _description_
        """
        tokens = input.txt.split()
        key = ""
        data: list[dict[str, str]] = []
        for item in tokens:
            if key:
                data.append({"key": key, "value": item})
                key = ""
            if item.endswith(":"):
                key = item
        if not data:
            self.parse_fail(msg="No key value pairs found.", input=input, ctx=ctx)

        parsed = ParsedIndexedString(
            id=self.parsed_state, indexed_string=input, data={"key_values": data}
        )
        result = ParseResult(
            parsed_state=self.parsed_state, parsed_indexed_string=parsed
        )
        return result


class NumberOfTokens(ParserABC):
    """NumberOfTokens.

    Args:
        ParserABC (_type_): _description_
    """

    def __init__(self, parsed_state: str, token_count: int) -> None:
        """__init__.

        Args:
            parsed_state (str): _description_
            token_count (int): The number of tokens expected in the input.
        """
        super().__init__(parsed_state)
        self.token_count = token_count

    def parse(self, ctx: P.ParseContext, input: IndexedStringProtocol) -> P.ParseResult:
        """Only matches when the number of tokens in the input is equal to the token_count.

        Args:
            ctx (P.ParseContext): _description_
            input (IndexedStringProtocol): _description_

        Returns:
            P.ParseResult: _description_
        """
        tokens = input.txt.split()

        if not len(tokens) == self.token_count:
            self.parse_fail(
                msg="Number of tokens does not match.", input=input, ctx=ctx
            )

        parsed = ParsedIndexedString(
            id=self.parsed_state, indexed_string=input, data={"tokens": tokens}
        )
        result = ParseResult(
            parsed_state=self.parsed_state, parsed_indexed_string=parsed
        )
        return result
