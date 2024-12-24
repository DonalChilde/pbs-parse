"""FILE: common.py."""

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from rich.progress import (
    BarColumn,
    FileSizeColumn,
    Progress,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TotalFileSizeColumn,
)

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
from pbs_parse.pbs_2022_01.split.extract_pages import parse_page_lines_from_file

progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    FileSizeColumn(),
    TotalFileSizeColumn(),
    TimeElapsedColumn(),
)
# pbs-parse data-store create ~/projects/tmp/store November 2024-11-01 2024-12-01
# pbs-parse data-store add-all-bases ~/projects/tmp/store ~/projects/tmp/pbs-data/2024.11.01-2024.12.01/


class ParseActions(StrEnum):
    """Possible parse actions."""

    SPLIT_TO_PAGES = "split_to_pages"
    SPLIT_TO_TRIPS = "split_to_trips"
    PARSE_TRIPS = "parse_trips"
    STRUCTURE_TRIPS = "structure_trips"
    EXPAND_TRIPS = "expand_trips"

    @staticmethod
    def action_list(
        start: "ParseActions",
        end: "ParseActions",
    ) -> list["ParseActions"]:
        """Get a list of the parse actions in order.

        Can also get an inclusive slice of the list.
        """
        action_list = list(ParseActions)
        start_index = action_list.index(start)
        end_index = action_list.index(end)
        if start_index > end_index:
            raise ValueError("Cannot perform actions in reverse order.")
        return action_list[start_index : end_index + 1]


@dataclass
class ActionItem:
    """Individual parse actions for ParseJob."""

    base: str
    action: ParseActions
    task_id: TaskID


@dataclass
class ParseJob:
    """Definition of a parse job, breaks down into action items."""

    base: str
    start: ParseActions = ParseActions.SPLIT_TO_PAGES
    end: ParseActions = ParseActions.EXPAND_TRIPS
    action_items: list[ActionItem] = field(default_factory=list)


def expand_actions(job: ParseJob) -> list[ActionItem]:
    """expand_actions.

    Args:
        job (ParseJob): _description_

    Returns:
        list[ActionItem]: _description_
    """
    parse_actions: list[ParseActions] = ParseActions.action_list(
        start=job.start, end=job.end
    )
    action_items: list[ActionItem] = []
    for parse_action in parse_actions:
        action_item = ActionItem(
            base=job.base,
            action=parse_action,
            task_id=progress.add_task(description=parse_action, total=None),
        )
        action_items.append(action_item)
    return action_items


def do_jobs(jobs: list[ParseJob], store: StoreManager) -> None:
    """do_jobs.

    Args:
        jobs (list[ParseJob]): _description_
        store (StoreManager): _description_
    """
    for job in jobs:
        with progress:
            for action in job.action_items:
                action_dispatch(action=action, store=store)


def action_dispatch(action: ActionItem, store: StoreManager):
    """action_dispatch.

    Args:
        action (ActionItem): _description_
        store (StoreManager): _description_
    """
    match action.action:
        case ParseActions.SPLIT_TO_PAGES:
            split_to_pages(base=action.base, store=store, task_id=action.task_id)
        case ParseActions.SPLIT_TO_TRIPS:
            pass
        case ParseActions.PARSE_TRIPS:
            pass
        case ParseActions.STRUCTURE_TRIPS:
            pass
        case ParseActions.EXPAND_TRIPS:
            pass


def split_to_pages(base: str, store: StoreManager, task_id: TaskID):
    """split_to_pages _summary_.

    Code to split pages, with rich progress.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    source_info = store.get_files(base=base, file_type=manifest.FileTypes.TXT_PACKAGE)
    source_path = source_info[0]["file_path"]
    progress.update(task_id=task_id, total=1, description="Splitting pages....")
    msg = f"Splitting pages from {source_path}"
    progress.console.print(msg)
    pages = parse_page_lines_from_file(path_in=Path(source_info[0]["file_path"]))
    count = store.save_page_lines(base=base, pages=pages)
    progress.update(
        task_id=task_id, completed=True, description=f"Found {count} pages."
    )
    msg = f"Found {count} pages in {source_path}"
    progress.console.print(msg)


def split_to_trips(base: str, store: StoreManager, task_id: TaskID):
    """split_to_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    page_infos = store.get_files(base=base, file_type=manifest.FileTypes.SPLIT_PAGE)


def parse_trips(base: str, store: StoreManager, task_id: TaskID):
    """parse_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """


def structure_trips(base: str, store: StoreManager, task_id: TaskID):
    """structure_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """


def expand_trips(base: str, store: StoreManager, task_id: TaskID):
    """expand_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
