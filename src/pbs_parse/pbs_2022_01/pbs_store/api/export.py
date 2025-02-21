"""FILE: export.py."""

from pathlib import Path

from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.pbs_store.store_manager import StoreManager

from . import load
from .get import expanded_errors_keys


def expanded_debug(
    store: StoreManager, base: str, dir_out: Path, overwrite: bool = False
) -> int:
    """expanded_debug.

    Args:
        store (StoreManager): _description_
        base (str): _description_
        dir_out (Path): _description_
        overwrite (bool, optional): _description_. Defaults to True.

    Returns:
        int: _description_
    """
    error_keys = expanded_errors_keys(store=store, base=base)
    error_count = len(error_keys)
    for key in error_keys:
        expanded = load.expanded_trip(store=store, base=base, key=key)
        parsed = load.parsed_trip(
            store=store, base=base, key=expanded.source.parsed_trip
        )
        API.save.expanded_debug(dir_out=dir_out, parsed=parsed, expanded=expanded)

    return error_count
