"""Some example result handlers."""

import json
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path
from types import TracebackType
from typing import Any, Self

from . import check_file
from . import protocol as P


class ResultHandlerABC(ABC):
    """ResultHandlerABC.

    A very simple ABC with the context manager boilerplate code.
    """

    def __init__(self) -> None:  # noqa: B027
        """__init__."""
        pass

    def __enter__(self) -> Self:  # noqa: D105
        return self

    def __exit__(  # noqa: D105
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        return None

    @abstractmethod
    def handle_result(
        self,
        ctx: P.ParseContext,
        parse_result: P.ParseResult,
    ) -> None:
        """Handle the result of a successful parse.

        Args:
            ctx: The ParseContext
            parse_result: The result of a successful parse.
        """
        raise NotImplementedError


class CollectResults(ResultHandlerABC):
    """CollectResults.

    Args:
        results (list[P.ParseResult]): the collected ParseResults of a parse job.
    """

    def __init__(self) -> None:
        """__init_."""
        super().__init__()
        self.results: list[P.ParseResult] = []

    def handle_result(
        self,
        ctx: P.ParseContext,
        parse_result: P.ParseResult,
    ) -> None:
        """Handle the result of a successful parse.

        Args:
            ctx: The ParseContext
            parse_result: The result of a successful parse.
        """
        self.results.append(parse_result)


class SaveParsedIndexedStringsToFile(CollectResults):
    """Save to json file just the `ParsedIndexedString`s from the collected ParseResults."""

    def __init__(
        self,
        path_out: Path,
        overwrite: bool = False,
        simplifier: Callable[[P.ParsedIndexedString], Any] | None = None,
    ) -> None:
        """__init__.

        Args:
            path_out (Path): _description_
            overwrite (bool, optional): _description_. Defaults to False.
            simplifier (Callable[[P.ParsedIndexedString], Any] | None, optional): A
                function that can turn the ParsedIndexedString into a json serializable
                object. If None, dataclass.asdict is used. Defaults to None.
        """
        super().__init__()
        self.path_out = path_out
        self.overwrite = overwrite
        self.simplifier = simplifier

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """Save to file on exit."""
        if check_file(path_out=self.path_out, overwrite=self.overwrite):
            if self.simplifier is not None:
                simplified = [
                    self.simplifier(x.parsed_indexed_string) for x in self.results
                ]
            else:
                simplified = [asdict(x.parsed_indexed_string) for x in self.results]  # type: ignore
            with open(self.path_out, mode="w") as file_out:
                json.dump(simplified, file_out, indent=1)


class SaveResultsToFile(CollectResults):
    """Save the collected ParseResults to json file.."""

    def __init__(
        self,
        path_out: Path,
        overwrite: bool = False,
        simplifier: Callable[[P.ParseResult], Any] | None = None,
    ) -> None:
        """__init__.

        Args:
            path_out (Path): _description_
            overwrite (bool, optional): _description_. Defaults to False.
            simplifier (Callable[[P.ParseResult], Any] | None, optional): A
                function that can turn the ParseResult into a json serializable
                object. If None, dataclass.asdict is used. Defaults to None.
        """
        super().__init__()
        self.path_out = path_out
        self.overwrite = overwrite
        self.simplifier = simplifier

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """Save to file on exit."""
        if check_file(path_out=self.path_out, overwrite=self.overwrite):
            if self.simplifier is not None:
                simplified = [self.simplifier(x) for x in self.results]
            else:
                simplified = [asdict(x) for x in self.results]  # type: ignore
            with open(self.path_out, mode="w") as file_out:
                json.dump(simplified, file_out, indent=1)
