"""FILE: bid_data.py."""

from pydantic import BaseModel, ConfigDict

from ...snippets.whenever.pydantic import PydanticDate


class Effective(BaseModel):
    """Effective."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    start: PydanticDate
    end: PydanticDate


class BidData(BaseModel):
    """BidData."""

    name: str
    base: str
    effective: Effective
