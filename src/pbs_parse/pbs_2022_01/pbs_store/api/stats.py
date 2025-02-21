"""FILE: stats.py."""

from collections.abc import Iterable, Sequence

from pbs_parse.pbs_2022_01.pbs_store.store_manager import StoreManager

from . import get, query


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
    stats.append(f"{get.name(store=store)}")
    for base in bases:
        stats.extend(
            f"{indent}{x}"
            for x in make_stats_base(store=store, base=base, indent=indent)
        )

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
    stats: list[str] = []
    stats.append(f"{base}:")
    stats.extend(
        [
            f"{indent}{x}"
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
    expanded_errors = query.expanded_trip_errors(store=store, base_name=base)
    stats.append(f"Errors:")
    stats.append(f"{indent}Number of trips with errors: {len(expanded_errors)}")
    if expanded_errors:
        stats.append(f"{indent}Expanded trip errors:")
        for key, value in expanded_errors.items():
            stats.append(f"{indent * 2}{key}")
            stats.extend([f"{indent * 3}{x}" for x in value])
    return stats
