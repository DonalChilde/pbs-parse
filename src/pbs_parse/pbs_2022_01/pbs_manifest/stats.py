"""FILE: stats.py."""

from collections.abc import Iterable, Sequence

from pbs_parse.pbs_2022_01.models.manifest import FileTypes
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

from . import load


def make_stats(store: StoreManager, bases: Iterable[str], indent: str = "  ") -> str:
    """make_stats.

    Args:
        store (StoreManager): _description_
        bases (Iterable[str]): _description_
        indent (str, optional): _description_. Defaults to "  ".

    Returns:
        str: _description_
    """
    stats: list[str] = []
    for base in bases:
        stats.extend(make_stats_base(store=store, base=base, indent=indent))

    return "\n".join(stats)


def make_stats_base(
    store: StoreManager, base: str, indent: str = "  "
) -> Sequence[str]:
    """make_stats_base.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        indent (str, optional): _description_. Defaults to "  ".

    Returns:
        Sequence[str]: _description_
    """
    trip_error_count = 0
    stats: list[str] = []
    stats.append(f"{base}:")
    stats.append(f"{indent}Errors:")
    stats.append(f"{indent*2}Number of trips with errors: {trip_error_count}")
    stats.extend(
        [
            f"{indent*2}{x}"
            for x in make_base_errors(base=base, store=store, indent=indent)
        ]
    )

    return stats


def make_base_errors(
    store: StoreManager, base: str, indent: str = "  "
) -> Sequence[str]:
    """make_base_errors.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        indent (str, optional): _description_. Defaults to "  ".

    Returns:
        Sequence[str]: _description_
    """
    stats: list[str] = []
    structured_error_infos = store.get_file_info_by_type(
        base=base, file_type=FileTypes.STRUCTURED_TRIP_VALIDATION
    )
    expanded_error_infos = store.get_file_info_by_type(
        base=base, file_type=FileTypes.EXPANDED_TRIP_VALIDATION
    )
    trip_error_count = len(structured_error_infos) + len(expanded_error_infos)
    stats.append(f"Errors:")
    stats.append(f"{indent}Number of trips with errors: {trip_error_count}")
    stats.append(f"{indent}Structured trip errors:")
    stats.extend(
        [
            f"{indent*2}{x}"
            for x in make_structured_trip_errors(store=store, base=base, indent=indent)
        ]
    )
    stats.append(f"{indent}Expanded trip errors:")
    stats.extend(
        [
            f"{indent*2}{x}"
            for x in make_expanded_trip_errors(store=store, base=base, indent=indent)
        ]
    )
    return stats


def make_structured_trip_errors(
    store: StoreManager, base: str, indent: str = "  "
) -> Sequence[str]:
    """make_structured_trip_errors.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        indent (str, optional): _description_. Defaults to "  ".

    Returns:
        Sequence[str]: _description_
    """
    stats: list[str] = []
    structured_error_infos = store.get_file_info_by_type(
        base=base, file_type=FileTypes.STRUCTURED_TRIP_VALIDATION
    )
    for info in structured_error_infos:
        validation = load.structured_trip_validation(
            store=store, base=base, uuid=info["key"]
        )
        s_trip = validation.structured
        stats.append(f"{s_trip.number}_{s_trip.idx}")
        for error in validation.errors:
            stats.append(f"{indent}{error}")
    return stats


def make_expanded_trip_errors(
    store: StoreManager, base: str, indent: str = "  "
) -> Sequence[str]:
    """make_expanded_trip_errors.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        indent (str, optional): _description_. Defaults to "  ".

    Returns:
        Sequence[str]: _description_
    """
    stats: list[str] = []
    expanded_error_infos = store.get_file_info_by_type(
        base=base, file_type=FileTypes.EXPANDED_TRIP_VALIDATION
    )
    for info in expanded_error_infos:
        validation = load.expanded_trip_validation(
            store=store, base=base, uuid=info["key"]
        )
        e_trip = validation.expanded
        stats.append(
            f"{e_trip.trip_number}_{e_trip.start_lcl.date()}_{e_trip.source_idx}"
        )
        for error in validation.errors:
            stats.append(f"{indent}{error}")
    return stats
