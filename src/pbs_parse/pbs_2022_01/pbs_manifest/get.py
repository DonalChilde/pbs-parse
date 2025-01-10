"""FILE: get.py."""

from datetime import date

from pbs_parse.pbs_2022_01.pbs_manifest.stats import make_stats
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager


def effective_dates(store: StoreManager) -> tuple[date, date]:
    """get_effective_dates _summary_.

    Returns:
        tuple[date, date]: (from,to)
    """
    return (
        date.fromisoformat(store.manifest["effective_from"]),
        date.fromisoformat(store.manifest["effective_to"]),
    )


def bases(store: StoreManager) -> list[str]:
    """Get a list of base keys."""
    return list(store.manifest["bases"].keys())


def name(store: StoreManager) -> str:
    """Get store name."""
    return store.manifest["name"]


def stats(store: StoreManager) -> str:
    """get_stats.

    Args:
        store (StoreManager): _description_

    Returns:
        str: _description_
    """
    _bases = bases(store=store)
    stats = make_stats(store=store, bases=_bases, indent="  ")
    return stats
