"""FILE: common.py."""

from enum import StrEnum

from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager


class ParseActions(StrEnum):
    """Possible parse actions."""

    SPLIT_TO_PAGES = "split_to_pages"
    SPLIT_TO_TRIPS = "split_to_trips"
    PARSE_TRIPS = "parse_trips"
    STRUCTURE_TRIPS = "structure_trips"
    EXPAND_TRIPS = "expand_trips"


class ParseJob:
    """Definition of a parse job, breaks down into parse items."""

    base: str
    start: ParseActions = ParseActions.SPLIT_TO_PAGES
    end: ParseActions = ParseActions.EXPAND_TRIPS


class ActionItem:
    """Individual parse actions for ParseJob."""

    base: str
    action: ParseActions


def action_dispatch(action: ActionItem, store: StoreManager):
    """Dispatch actions here."""


def split_to_pages(base: str, store: StoreManager):
    """split_to_pages _summary_.

    Code to split pages, with rich progress.

    Args:
        base (str): _description_
        store (StoreManager): _description_
    """


def split_to_trips(base: str, store: StoreManager):
    """split_to_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
    """


def parse_trips(base: str, store: StoreManager):
    """parse_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
    """


def structure_trips(base: str, store: StoreManager):
    """structure_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
    """


def expand_trips(base: str, store: StoreManager):
    """expand_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
    """
