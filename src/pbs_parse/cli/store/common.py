"""FILE: common.py."""

from dataclasses import dataclass, field
from enum import StrEnum

from rich.progress import TaskID

import pbs_parse.pbs_2022_01.pbs_manifest as STORE

from ..work.expand_trips import expand_trips_store
from ..work.parse_trips import parse_trips_store
from ..work.progress import progress
from ..work.split_to_pages import split_to_pages_store
from ..work.split_to_trips import split_to_trips_store
from ..work.structure_trips import structure_trips_store
from ..work.validate_expanded import validate_expanded_store
from ..work.validate_structured import validate_structured_store

# pbs-parse data-store create ~/projects/tmp/store November 2024-11-01 2024-12-01
# pbs-parse data-store add-all-bases ~/projects/tmp/store ~/projects/tmp/pbs-data/2024.11.01-2024.12.01/
# pbs-parse data-store parse-all ~/projects/tmp/store


class ParseActions(StrEnum):
    """Possible parse actions."""

    SPLIT_TO_PAGES = "split_to_pages"
    SPLIT_TO_TRIPS = "split_to_trips"
    PARSE_TRIPS = "parse_trips"
    STRUCTURE_TRIPS = "structure_trips"
    VALIDATE_STRUCTURED_TRIPS = "validate_structured_trips"
    EXPAND_TRIPS = "expand_trips"
    VALIDATE_EXPANDED_TRIPS = "validate_expanded_trips"

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


@dataclass(slots=True)
class ActionItem:
    """Individual parse actions for ParseJob."""

    base: str
    action: ParseActions
    task_id: TaskID
    overwrite: bool = False


@dataclass(slots=True)
class ParseJob:
    """Definition of a parse job, breaks down into action items."""

    base: str
    start: ParseActions = ParseActions.SPLIT_TO_PAGES
    end: ParseActions = ParseActions.VALIDATE_EXPANDED_TRIPS
    overwrite: bool = False
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
            task_id=progress.add_task(description=">>>Waiting<<<", total=None),
        )
        action_items.append(action_item)
    job.action_items = action_items
    return action_items


def do_jobs(jobs: list[ParseJob], store: STORE.StoreManager) -> None:
    """do_jobs.

    Args:
        jobs (list[ParseJob]): _description_
        store (StoreManager): _description_
    """
    store_name = STORE.get.name(store=store)
    for job in jobs:
        with progress:
            task_id = progress.add_task(
                description=f"[blue]..... {store_name}-{job.base} ....."
            )
            expand_actions(job=job)
            progress.update(task_id=task_id, total=len(job.action_items))
            for action in job.action_items:
                action_dispatch(action=action, store=store)
                progress.update(task_id=task_id, advance=1)


def action_dispatch(action: ActionItem, store: STORE.StoreManager):
    """action_dispatch.

    Args:
        action (ActionItem): _description_
        store (StoreManager): _description_
    """
    match action.action:
        case ParseActions.SPLIT_TO_PAGES:
            split_to_pages_store(
                base=action.base,
                store=store,
                task_id=action.task_id,
                progress=progress,
                overwrite=action.overwrite,
            )
        case ParseActions.SPLIT_TO_TRIPS:
            split_to_trips_store(
                base=action.base,
                store=store,
                task_id=action.task_id,
                progress=progress,
                overwrite=action.overwrite,
            )
        case ParseActions.PARSE_TRIPS:
            parse_trips_store(
                base=action.base,
                store=store,
                task_id=action.task_id,
                progress=progress,
                overwrite=action.overwrite,
            )
        case ParseActions.STRUCTURE_TRIPS:
            structure_trips_store(
                base=action.base,
                store=store,
                task_id=action.task_id,
                progress=progress,
                overwrite=action.overwrite,
            )
        case ParseActions.VALIDATE_STRUCTURED_TRIPS:
            validate_structured_store(
                base=action.base,
                store=store,
                task_id=action.task_id,
                progress=progress,
                overwrite=action.overwrite,
            )
        case ParseActions.EXPAND_TRIPS:
            expand_trips_store(
                base=action.base,
                store=store,
                task_id=action.task_id,
                progress=progress,
                overwrite=action.overwrite,
            )
        case ParseActions.VALIDATE_EXPANDED_TRIPS:
            validate_expanded_store(
                base=action.base,
                store=store,
                task_id=action.task_id,
                progress=progress,
                overwrite=action.overwrite,
            )
