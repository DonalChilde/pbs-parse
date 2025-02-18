"""pages lines."""

from pydantic import BaseModel

from pbs_parse.pbs_2022_01.models.bid_data import BidData
from pbs_parse.snippets.indexed_string.pydantic_model import IndexedString


class PageLinesSource(BaseModel):
    """PageLinesSource."""

    txt_file: str = "TXT_FILE"


class PageLines(BaseModel):
    """PageLines."""

    source: PageLinesSource
    """The source of the page_lines."""
    bid: BidData
    """The details of the bid package that the page falls in."""
    idx: str
    """The index of the page as it was parsed from the bid package. Starts at 00001-00.
    The -00 suffix is a place holder for the indexes of trips found in the page."""
    lines: list[IndexedString]
    """The indexed lines of text found in the page."""

    def default_file_name(self) -> str:
        """default_file_name.

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
        return f"page-lines_{bid.name}_{bid.base}_{idx}.json"
