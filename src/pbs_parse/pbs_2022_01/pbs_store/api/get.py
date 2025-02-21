"""FILE: get.py."""

from whenever import Date

from pbs_parse.pbs_2022_01.pbs_store.store_manager import StoreManager

from .stats import make_stats


def effective_dates(store: StoreManager) -> tuple[Date, Date]:
    """effective_dates.

    Args:
        store (StoreManager): _description_

    Returns:
        tuple[Date, Date]: (from,to))
    """
    return (store.manifest.effective_from, store.manifest.effective_to)


def bases(store: StoreManager) -> list[str]:
    """Get a list of base keys."""
    return list(store.manifest.bases.keys())


def name(store: StoreManager) -> str:
    """Get store name."""
    return store.manifest.name


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


def expanded_errors_keys(store: StoreManager, base_name: str) -> list[str]:
    """Get a list of expanded trip keys with errors."""
    base = store.get_base(base_name=base_name)
    base_errors = base.details.expanded_errors
    return list(base_errors.keys())
