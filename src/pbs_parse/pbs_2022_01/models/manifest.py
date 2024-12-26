"""Models for the various manifest data structures."""

from enum import StrEnum
from typing import TypedDict


class FileTypes(StrEnum):
    """The different file types that can be listed in a manifest."""

    SPLIT_PAGE = "split_page"
    SPLIT_TRIP = "split_trip"
    PARSED_TRIP = "parsed_trip"
    PARSED_PRIOR_MONTH_TRIP = "parsed_prior_month_trip"
    STRUCTURED_TRIP = "structured_trip"
    EXPANDED_TRIP = "expanded_trip"
    PDF_PACKAGE = "pdf_package"
    TXT_PACKAGE = "txt_package"
    BID_MANIFEST = "bid_manifest"
    ERROR_MSG = "error_msg"
    ALL = "all"


class FileInfo(TypedDict):
    """Info for an item in the store."""

    key: str
    type: str
    file_path: str


class Base(TypedDict):
    """Base info."""

    base_name: str
    files: dict[str, FileInfo]


class BidPeriodManifest(TypedDict):
    """Manifest for all the bids in a month."""

    name: str
    effective_from: str
    effective_to: str
    bases: dict[str, Base]
