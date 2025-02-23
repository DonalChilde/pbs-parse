"""Models for the various manifest data structures."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict

from pbs_parse.snippets.whenever.pydantic import PydanticDate


class FileInfo(BaseModel):
    """Info for an item in the store."""

    key: str
    file_path: Path


class Base(BaseModel):
    """Base info."""

    base_name: str
    source_pdf: FileInfo
    source_txt: FileInfo
    pages: dict[str, FileInfo] = {}
    raw_trips: dict[str, FileInfo] = {}
    prior_month_raw_trips: dict[str, FileInfo] = {}
    parsed_trips: dict[str, FileInfo] = {}
    expanded_trips: dict[str, FileInfo] = {}
    expanded_trips_with_errors: set[str] = set()


class BidPeriodManifest(BaseModel):
    """Manifest for all the bids in a month."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    effective_from: PydanticDate
    effective_to: PydanticDate
    bases: dict[str, Base]
