"""Models for Parsed trips."""

from pydantic import BaseModel, ConfigDict

from pbs_parse.pbs_2022_01.models.bid_data import BidData
from pbs_parse.snippets.indexed_string_state_parser.pydantic_model import (
    ParsedIndexedString,
)

from .pydantic import PydanticDate


class ParsedTripSource(BaseModel):
    """ParsedTripSource."""

    txt_file: str = "TXT_FILE"
    page_lines: str = "PAGE_LINES"
    trip_lines: str = "TRIP_LINES"


class ParsedTrip(BaseModel):
    """ParsedTrip contains the parsed lines of a pbs trip."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    source: ParsedTripSource
    bid: BidData
    idx: str
    parsed_lines: list[ParsedIndexedString]
    calendar_entries: list[str] = []
    start_dates: list[PydanticDate] = []
    errors: list[str] = []

    def default_file_name(self) -> str:
        """default_file_name.

        Args:
            page_idx (int): _description_
            trip_idx (int): _description_

        Returns:
            str: _description_
        """
        return self.assemble_file_name(idx=self.idx, bid=self.bid)

    @staticmethod
    def assemble_file_name(idx: str, bid: BidData) -> str:
        """assemble_file_name.

        Args:
            idx (str): _description_
            bid (BidData): _description_

        Returns:
            str: _description_
        """
        return f"parsed-trip_{bid.name}_{bid.base}_{idx}.json"

    def original_text(self, with_line_num: bool = True, sep: str = "") -> str:
        """Get the original input text, with and without line numbers."""
        if with_line_num:
            return f"{sep.join([f'[{x.indexed_string.idx:06}] {x.indexed_string.txt}' for x in self.parsed_lines])}\n"
        else:
            return (
                f"{sep.join([f'{x.indexed_string.txt}' for x in self.parsed_lines])}\n"
            )

    def __str__(self) -> str:
        """Make a str rep of ParsedTrip."""
        return (
            "ParsedTrip:\n"
            f"{self.idx=}\n"
            f"{self.source=}\n"
            f"Errors: {len(self.errors)}\n"
            f"{'\n'.join(self.errors)}"
            "\nText Input:\n"
            f"{self.original_text()}"
            "Parsed Data:\n"
            f"{'\n'.join([f'{x.id:20}[{x.indexed_string.idx:06}] {x.data!r}' for x in self.parsed_lines])}\n"
        )
