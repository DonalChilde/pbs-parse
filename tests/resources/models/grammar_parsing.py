"""Model to hold elements of a grammar parsing test."""

from dataclasses import dataclass

from pyparsing import ParserElement


@dataclass(slots=True)
class GrammarParsingTest[T]:
    """Contains input and result data for a test."""

    txt: str
    parser: ParserElement
    result: T
    description: str = ""
