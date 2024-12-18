"""Models for the various manifest data structures."""

from enum import StrEnum
from typing import TypedDict


class FileTypes(StrEnum):
    """The different file types that can be listed in a manifest."""

    SPLIT_PAGE = "split_page"
    SPLIT_TRIP = "split_trip"
    PARSED_TRIP = "parsed_trip"
    STRUCTURED_TRIP = "structured_trip"
    EXPANDED_TRIP = "expanded_trip"
    PDF_PACKAGE = "pdf_package"
    TXT_PACKAGE = "txt_package"
    BID_MANIFEST = "bid_manifest"


class FileInfo(TypedDict):
    """Info for an item in the store."""

    uuid: str
    type: str
    file_name: str


class Base(TypedDict):
    """Base info."""

    base_name: str
    source_file: str
    source_dir: str
    split_page_dir: str
    split_trip_dir: str
    parsed_trip_dir: str
    structured_trip_dir: str
    expanded_trip_dir: str
    files: list[FileInfo]


class BidPeriodManifest(TypedDict):
    """Manifest for all the bids in a month."""

    name: str
    effective_from: str
    effective_to: str
    bases: list[Base]
