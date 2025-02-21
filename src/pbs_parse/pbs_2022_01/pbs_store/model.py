"""Models for the various manifest data structures."""

from pathlib import Path

from pydantic import BaseModel

from pbs_parse.snippets.whenever.pydantic import PydanticDate, PydanticTimeDelta

# class FileTypes(StrEnum):
#     """The different file types that can be listed in a manifest."""

#     SPLIT_PAGE = "split_page"
#     SPLIT_TRIP = "split_trip"
#     SPLIT_TRIP_PRIOR = "split_trip_prior"
#     PARSED_TRIP = "parsed_trip"
#     EXPANDED_TRIP = "expanded_trip"
#     PDF_PACKAGE = "pdf_package"
#     TXT_PACKAGE = "txt_package"
#     BID_MANIFEST = "bid_manifest"
#     ALL = "all"


# TODO make this a generic for `type`. esp. if the Store gets snippeted.
class FileInfo(BaseModel):
    """Info for an item in the store."""

    key: str
    file_path: Path


class ExpandedTripStatistics:
    """A collection of precalculated statistics for ExpandedTrips."""

    flight_time: PydanticTimeDelta
    operating_time: PydanticTimeDelta
    soft_time: PydanticTimeDelta
    tafb: PydanticTimeDelta
    duty_periods: int
    calendar_days: int


class BaseDetails(BaseModel):
    """Details pulled from parsed and expanded Trips."""

    expanded_errors: dict[str, list[str]]
    satellite_bases: set[str]
    equipment: set[str]
    expanded_trips_by_base: dict[str, str]
    expanded_trips_by_equipment: dict[str, str]
    expanded_trip_statistics: dict[str, ExpandedTripStatistics]


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
    details: BaseDetails | None = None


class BidPeriodManifest(BaseModel):
    """Manifest for all the bids in a month."""

    name: str
    effective_from: PydanticDate
    effective_to: PydanticDate
    bases: dict[str, Base]
