"""FILE: save.py."""

from pathlib import Path

from pbs_parse.pbs_2022_01.models.expanded import EXPANDED_TRIP_SERIALIZER, ExpandedTrip
from pbs_parse.pbs_2022_01.models.expanded_validation import (
    EXPANDED_VALIDATION_SERIALIZER,
    ExpandedValidation,
)
from pbs_parse.pbs_2022_01.models.manifest import FileInfo, FileTypes
from pbs_parse.pbs_2022_01.models.page_lines import PAGE_LINES_SERIALIZER, PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER, ParsedTrip
from pbs_parse.pbs_2022_01.models.structured import (
    STRUCTURED_TRIP_SERIALIZER,
    StructuredTrip,
)
from pbs_parse.pbs_2022_01.models.structured_validation import (
    STRUCTURED_VALIDATION_SERIALIZER,
    StructuredValidation,
)
from pbs_parse.pbs_2022_01.models.trip_lines import TRIP_LINES_SERIALIZER, TripLines
from pbs_parse.pbs_2022_01.pbs_manifest.exceptions import (
    StoreOperationError,
)
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager


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


def parsed_prior_month_trip(
    store: StoreManager, base: str, parsed: ParsedTrip, overwrite: bool = False
) -> Path:
    """Save a ParsedTrip in the store."""
    if store.read_only:
        raise StoreOperationError(
            "Store is opened in read-only mode. No changes allowed."
        )
    trip_info = FileInfo(
        key=parsed.default_file_name(),
        type=FileTypes.PARSED_PRIOR_MONTH_TRIP,
        file_path=f"{base}/parsed_prior/{parsed.default_file_name()}",
    )
    path_out = store.manifest_directory / trip_info["file_path"]
    PARSED_TRIP_SERIALIZER.save_as_json(
        path_out=path_out, complex_obj=parsed, overwrite=overwrite
    )
    store.record_file(base=base, info=trip_info)
    return path_out


def structured_trip(
    store: StoreManager, base: str, structured: StructuredTrip, overwrite: bool = False
) -> Path:
    """Save a StructuredTrip in the store."""
    if store.read_only:
        raise StoreOperationError(
            "Store is opened in read-only mode. No changes allowed."
        )
    trip_info = FileInfo(
        key=structured.default_file_name(),
        type=FileTypes.STRUCTURED_TRIP,
        file_path=f"{base}/structured/{structured.default_file_name()}",
    )
    path_out = store.manifest_directory / trip_info["file_path"]
    STRUCTURED_TRIP_SERIALIZER.save_as_json(
        path_out=path_out, complex_obj=structured, overwrite=overwrite
    )
    store.record_file(base=base, info=trip_info)
    return path_out


def structured_trip_validation_error(
    store: StoreManager,
    base: str,
    validation_model: StructuredValidation,
    overwrite: bool = False,
) -> Path:
    """Fix type of error."""
    if store.read_only:
        raise StoreOperationError(
            "Store is opened in read-only mode. No changes allowed."
        )
    trip_info = FileInfo(
        key=validation_model.default_file_name(),
        type=FileTypes.STRUCTURED_TRIP_VALIDATION,
        file_path=f"{base}/structured/errors/{validation_model.default_file_name()}",
    )
    path_out = store.manifest_directory / trip_info["file_path"]
    STRUCTURED_VALIDATION_SERIALIZER.save_as_json(
        path_out=path_out, complex_obj=validation_model, overwrite=overwrite
    )
    store.record_file(base=base, info=trip_info)
    return path_out


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
    return path_out


def expanded_trip_validation_error(
    store: StoreManager,
    base: str,
    validation_model: ExpandedValidation,
    overwrite: bool = False,
) -> Path:
    """Fix type of error."""
    if store.read_only:
        raise StoreOperationError(
            "Store is opened in read-only mode. No changes allowed."
        )
    trip_info = FileInfo(
        key=validation_model.default_file_name(),
        type=FileTypes.EXPANDED_TRIP_VALIDATION,
        file_path=f"{base}/expanded/errors/{validation_model.default_file_name()}",
    )
    path_out = store.manifest_directory / trip_info["file_path"]
    EXPANDED_VALIDATION_SERIALIZER.save_as_json(
        path_out=path_out, complex_obj=validation_model, overwrite=overwrite
    )
    store.record_file(base=base, info=trip_info)
    return path_out
