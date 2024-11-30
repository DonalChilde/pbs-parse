"""Models for the various manifest data structures."""

from dataclasses import dataclass, field
from enum import StrEnum


class FileTypes(StrEnum):
    """The different file types that can be listed in a manifest."""

    SPLIT_PAGE = "split_page"
    SPLIT_TRIP = "split_trip"
    PARSED_TRIP = "parsed_trip"
    STRUCTURED_TRIP = "structured_trip"
    PDF_PACKAGE = "pdf_package"
    TXT_PACKAGE = "txt_package"
    BID_MANIFEST = "bid_manifest"


@dataclass(slots=True)
class FileInfo:
    """Info for an item in the store."""

    uuid: str
    type: str
    path: str


@dataclass(slots=True)
class BidMonthManifest:
    """Manifest for all the bids in a month."""

    pass


@dataclass(slots=True)
class StoreManifest:
    """Manifest for all the bids in the store."""

    bid_months: list[BidMonthManifest] = field(default_factory=list)
