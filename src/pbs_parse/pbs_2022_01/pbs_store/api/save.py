"""FILE: save.py."""

from copy import deepcopy
from pathlib import Path

from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.page_lines import PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines
from pbs_parse.pbs_2022_01.pbs_store.model import FileInfo
from pbs_parse.pbs_2022_01.pbs_store.store_manager import StoreManager


def page_lines(
    store: StoreManager, base_name: str, page: PageLines, overwrite: bool = False
) -> Path:
    """Save a PageLines in the store."""
    store.read_only_check()
    base = store.get_base(base_name=base_name)
    file_info = FileInfo(
        key=page.default_file_name(),
        file_path=Path(f"{base_name}/pages/{page.default_file_name()}"),
    )
    path_out = store.manifest_directory / file_info.file_path
    API.save.page_lines(
        dir_out=path_out.parent,
        file_name=path_out.name,
        page_lines=page,
        overwrite=overwrite,
    )
    base.pages[file_info.key] = file_info
    return path_out


def trip_lines(
    store: StoreManager,
    base_name: str,
    trip: TripLines,
    overwrite: bool = False,
):
    """Save TripLines in the store."""
    store.read_only_check()
    base = store.get_base(base_name=base_name)
    file_info = FileInfo(
        key=trip.default_file_name(),
        file_path=Path(f"{base_name}/trip_lines/{trip.default_file_name()}"),
    )
    path_out = store.manifest_directory / file_info.file_path
    API.save.trip_lines(
        dir_out=path_out.parent,
        file_name=path_out.name,
        trip_lines=trip,
        overwrite=overwrite,
    )
    base.raw_trips[file_info.key] = file_info
    return path_out


def trip_lines_prior(
    store: StoreManager,
    base_name: str,
    trip: TripLines,
    overwrite: bool = False,
):
    """Save prior month TripLines in the store."""
    store.read_only_check()
    base = store.get_base(base_name=base_name)
    file_info = FileInfo(
        key=trip.default_file_name(),
        file_path=Path(f"{base_name}/trip_lines/prior/{trip.default_file_name()}"),
    )
    path_out = store.manifest_directory / file_info.file_path
    API.save.trip_lines(
        dir_out=path_out.parent,
        file_name=path_out.name,
        trip_lines=trip,
        overwrite=overwrite,
    )
    base.prior_month_raw_trips[file_info.key] = file_info
    return path_out


def parsed_trip(
    store: StoreManager, base_name: str, parsed: ParsedTrip, overwrite: bool = False
) -> Path:
    """Save a ParsedTrip in the store."""
    store.read_only_check()
    base = store.get_base(base_name=base_name)
    file_info = FileInfo(
        key=parsed.default_file_name(),
        file_path=Path(f"{base_name}/parsed/{parsed.default_file_name()}"),
    )
    path_out = store.manifest_directory / file_info.file_path
    API.save.parsed_trip(
        dir_out=path_out.parent,
        file_name=path_out.name,
        parsed_trip=parsed,
        overwrite=overwrite,
    )
    base.parsed_trips[file_info.key] = file_info
    return path_out


def expanded_trip(
    store: StoreManager, base_name: str, expanded: ExpandedTrip, overwrite: bool = False
) -> Path:
    """Save an ExpandedTrip in the store."""
    store.read_only_check()
    base = store.get_base(base_name=base_name)
    file_info = FileInfo(
        key=expanded.default_file_name(),
        file_path=Path(f"{base_name}/expanded/{expanded.default_file_name()}"),
    )
    path_out = store.manifest_directory / file_info.file_path
    API.save.expanded_trip(
        dir_out=path_out.parent,
        file_name=path_out.name,
        expanded_trip=expanded,
        overwrite=overwrite,
    )
    base.expanded_trips[file_info.key] = file_info
    if expanded.errors:
        _expanded_trip_errors(
            store=store,
            base_name=base_name,
            key=file_info.key,
            errors=expanded.errors,
        )
    return path_out


def _expanded_trip_errors(
    store: StoreManager, base_name: str, key: str, errors: list[str]
):
    """Save a copy of the errors found in an expanded trip in the store manifest.

    key should be the default file name for the expanded trip.
    """
    store.read_only_check()
    base = store.get_base(base_name=base_name)
    # TODO init details?

    base.details.expanded_errors[key] = deepcopy(errors)
