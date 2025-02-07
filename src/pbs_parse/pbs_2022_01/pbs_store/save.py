"""FILE: save.py."""

from copy import deepcopy
from pathlib import Path

from pbs_parse.pbs_2022_01.models.expanded import EXPANDED_TRIP_SERIALIZER, ExpandedTrip
from pbs_parse.pbs_2022_01.models.manifest import FileInfo, FileTypes
from pbs_parse.pbs_2022_01.models.page_lines import PAGE_LINES_SERIALIZER, PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER, ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TRIP_LINES_SERIALIZER, TripLines
from pbs_parse.pbs_2022_01.pbs_store.exceptions import (
    StoreOperationError,
)
from pbs_parse.pbs_2022_01.pbs_store.store_manager import StoreManager


def page_lines(
    store: StoreManager, base: str, page: PageLines, overwrite: bool = False
) -> Path:
    """Save a PageLines in the store."""
    if store.read_only:
        raise StoreOperationError(
            "Store is opened in read-only mode. No changes allowed."
        )
    page_info = FileInfo(
        key=page.default_file_name(),
        type=FileTypes.SPLIT_PAGE,
        file_path=f"{base}/pages/{page.default_file_name()}",
    )
    path_out = store.manifest_directory / page_info["file_path"]
    PAGE_LINES_SERIALIZER.save_as_json(
        path_out=path_out, complex_obj=page, overwrite=overwrite
    )
    store.record_file(base=base, info=page_info)
    return path_out


def trip_lines(
    store: StoreManager,
    base: str,
    trip: TripLines,
    overwrite: bool = False,
):
    """Save TripLines in the store."""
    if store.read_only:
        raise StoreOperationError(
            "Store is opened in read-only mode. No changes allowed."
        )
    trip_info = FileInfo(
        key=trip.default_file_name(),
        type=FileTypes.SPLIT_TRIP,
        file_path=f"{base}/trip_lines/{trip.default_file_name()}",
    )
    path_out = store.manifest_directory / trip_info["file_path"]
    TRIP_LINES_SERIALIZER.save_as_json(
        path_out=path_out, complex_obj=trip, overwrite=overwrite
    )
    store.record_file(base=base, info=trip_info)
    return path_out


def trip_lines_prior(
    store: StoreManager,
    base: str,
    trip: TripLines,
    overwrite: bool = False,
):
    """Save prior month TripLines in the store."""
    if store.read_only:
        raise StoreOperationError(
            "Store is opened in read-only mode. No changes allowed."
        )
    trip_info = FileInfo(
        key=trip.default_file_name(),
        type=FileTypes.SPLIT_TRIP_PRIOR,
        file_path=f"{base}/trip_lines/prior/{trip.default_file_name()}",
    )
    path_out = store.manifest_directory / trip_info["file_path"]
    TRIP_LINES_SERIALIZER.save_as_json(
        path_out=path_out, complex_obj=trip, overwrite=overwrite
    )
    store.record_file(base=base, info=trip_info)
    return path_out


def parsed_trip(
    store: StoreManager, base: str, parsed: ParsedTrip, overwrite: bool = False
) -> Path:
    """Save a ParsedTrip in the store."""
    if store.read_only:
        raise StoreOperationError(
            "Store is opened in read-only mode. No changes allowed."
        )
    trip_info = FileInfo(
        key=parsed.default_file_name(),
        type=FileTypes.PARSED_TRIP,
        file_path=f"{base}/parsed/{parsed.default_file_name()}",
    )
    path_out = store.manifest_directory / trip_info["file_path"]
    PARSED_TRIP_SERIALIZER.save_as_json(
        path_out=path_out, complex_obj=parsed, overwrite=overwrite
    )
    store.record_file(base=base, info=trip_info)
    return path_out


# def parsed_prior_month_trip(
#     store: StoreManager, base: str, parsed: ParsedTrip, overwrite: bool = False
# ) -> Path:
#     """Save a ParsedTrip in the store."""
#     if store.read_only:
#         raise StoreOperationError(
#             "Store is opened in read-only mode. No changes allowed."
#         )
#     trip_info = FileInfo(
#         key=parsed.default_file_name(),
#         type=FileTypes.PARSED_PRIOR_MONTH_TRIP,
#         file_path=f"{base}/parsed_prior/{parsed.default_file_name()}",
#     )
#     path_out = store.manifest_directory / trip_info["file_path"]
#     PARSED_TRIP_SERIALIZER.save_as_json(
#         path_out=path_out, complex_obj=parsed, overwrite=overwrite
#     )
#     store.record_file(base=base, info=trip_info)
#     return path_out


def expanded_trip(
    store: StoreManager, base: str, expanded: ExpandedTrip, overwrite: bool = False
) -> Path:
    """Save an ExpandedTrip in the store."""
    if store.read_only:
        raise StoreOperationError(
            "Store is opened in read-only mode. No changes allowed."
        )
    trip_info = FileInfo(
        key=expanded.default_file_name(),
        type=FileTypes.EXPANDED_TRIP,
        file_path=f"{base}/expanded/{expanded.default_file_name()}",
    )
    path_out = store.manifest_directory / trip_info["file_path"]
    EXPANDED_TRIP_SERIALIZER.save_as_json(
        path_out=path_out, complex_obj=expanded, overwrite=overwrite
    )
    store.record_file(base=base, info=trip_info)
    if expanded.errors:
        _expanded_trip_errors(
            store=store, base=base, key=trip_info["key"], errors=expanded.errors
        )
    return path_out


def _expanded_trip_errors(store: StoreManager, base: str, key: str, errors: list[str]):
    """Save a copy of the errors found in an expanded trip in the store manifest.

    key should be the default file name for the expanded trip.
    """
    if store.read_only:
        raise StoreOperationError(
            "Store is opened in read-only mode. No changes allowed."
        )
    expanded_errors_dict = store.manifest["bases"][base]["errors"].get(
        FileTypes.EXPANDED_TRIP, {}
    )
    expanded_errors_dict[key] = deepcopy(errors)
    store.manifest["bases"][base]["errors"][FileTypes.EXPANDED_TRIP] = (
        expanded_errors_dict
    )
