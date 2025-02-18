"""trip lines.."""

from pydantic import BaseModel

from pbs_parse.pbs_2022_01.models.bid_data import BidData
from pbs_parse.snippets.indexed_string.pydantic_model import IndexedString


class TripLinesSource(BaseModel):
    """TripLinesSource."""

    txt_file: str = "TXT_FILE"
    page_lines: str = "PAGE_LINES"


class TripLines(BaseModel):
    """TripLines."""

    source: TripLinesSource
    bid: BidData
    idx: str
    lines: list[IndexedString]

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
        return f"trip-lines_{bid.name}_{bid.base}_{idx}.json"


def is_prior_month(trip: TripLines) -> bool:
    """Check to see if the trip is a prior month trip."""
    if "prior" in trip.lines[2].txt:
        return True
    return False
