"""FILE: common.py."""

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum

from pfmsoft.state_parser import ParseContext
from rich.progress import TaskID

from pbs_parse.pbs_2022_01.expand.structured_to_expanded_cls import StructuredToExpanded
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.parsed_trip import (
    ParsedTrip,
)
from pbs_parse.pbs_2022_01.parse.trip_lines_parser import TripLinesParser
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
from pbs_parse.pbs_2022_01.split.extract_trips import (
    parse_trip_lines_from_file,
)
from pbs_parse.pbs_2022_01.structure.parsed_to_structured import (
    structure_trip_from_file,
)

from .progress import progress
from .split_to_pages import split_to_pages

# from pbs_parse.pbs_2022_01.validate.validate_structured import (
#     validate_structured_trip_from_file,
# )


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


def split_to_trips(base: str, store: StoreManager, task_id: TaskID):
    """split_to_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    page_infos = store.get_files_by_type(
        base=base, file_type=manifest.FileTypes.SPLIT_PAGE
    )
    progress.update(
        task_id=task_id, total=len(page_infos), description="Splitting trips...."
    )
    page_count = len(page_infos)
    total_trips = 0
    for page_idx, page in enumerate(page_infos, start=1):
        path_in = store.manifest_path / page["file_path"]
        trips = parse_trip_lines_from_file(path_in=path_in)
        count = store.save_trip_lines(base=base, trips=trips)
        total_trips += count
        progress.update(
            task_id=task_id,
            advance=count,
            description=f"Page {page_idx} of {page_count}, {total_trips} trips found.",
        )


def parse_trips(base: str, store: StoreManager, task_id: TaskID):
    """parse_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    trip_infos = store.get_files_by_type(
        base=base, file_type=manifest.FileTypes.SPLIT_TRIP
    )
    progress.update(
        task_id=task_id, total=len(trip_infos), description="Parsing trips...."
    )
    trip_count = len(trip_infos)
    total_trips = 0
    prior_trips = 0
    parser = TripLinesParser()
    for trip_idx, trip in enumerate(trip_infos, start=1):
        ctx = ParseContext()
        path_in = store.manifest_path / trip["file_path"]
        parsed_trip = parser.parse_file(ctx=ctx, path_in=path_in)
        if check_for_prior_month(parsed_trip=parsed_trip):
            store.save_parsed_prior_month_trip(base=base, parsed=parsed_trip)
            prior_trips += 1
        else:
            store.save_parsed_trip(base=base, parsed=parsed_trip)
            total_trips += 1
        progress.update(
            task_id=task_id,
            advance=1,
            description=f"Trip {trip_idx} of {trip_count}, {total_trips} trips parsed, with {prior_trips} prior month trips.",
        )


def structure_trips(base: str, store: StoreManager, task_id: TaskID):
    """structure_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    trip_infos = store.get_files_by_type(
        base=base, file_type=manifest.FileTypes.PARSED_TRIP
    )
    progress.update(
        task_id=task_id, total=len(trip_infos), description="Structuring trips...."
    )
    trip_count = len(trip_infos)
    total_trips = 0
    effective_from = date.fromisoformat(store.manifest["effective_from"])
    effective_to = date.fromisoformat(store.manifest["effective_to"])
    for trip_idx, trip in enumerate(trip_infos, start=1):
        path_in = store.manifest_path / trip["file_path"]
        structured_trip = structure_trip_from_file(
            path_in=path_in,
            effective_from=effective_from,
            effective_to=effective_to,
        )

        store.save_structured_trip(base=base, structured=structured_trip)
        total_trips += 1
        progress.update(
            task_id=task_id,
            advance=1,
            description=f"Trip {trip_idx} of {trip_count}, {total_trips} trips structured.",
        )


def validate_structured_trips(base: str, store: StoreManager, task_id: TaskID):
    """validate_structured_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    pass


def expand_trips(base: str, store: StoreManager, task_id: TaskID):
    """expand_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    s_trip_infos = store.get_files_by_type(
        base=base, file_type=manifest.FileTypes.STRUCTURED_TRIP
    )
    progress.update(
        task_id=task_id, total=len(s_trip_infos), description="Expanding trips...."
    )
    trip_count = len(s_trip_infos)
    total_trips = 0

    for trip_idx, s_trip in enumerate(s_trip_infos, start=1):
        path_in = store.manifest_path / s_trip["file_path"]
        translator = StructuredToExpanded.from_file(path_in=path_in)
        expanded_trips = translator.translate()

        count = store.save_expanded_trips(base=base, expanded=expanded_trips)
        total_trips += count
        progress.update(
            task_id=task_id,
            advance=1,
            description=f"Trip {trip_idx} of {trip_count}, {total_trips} trips expanded.",
        )


def validate_expanded_trips(base: str, store: StoreManager, task_id: TaskID):
    """validate_expanded_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    pass


def check_for_prior_month(parsed_trip: ParsedTrip) -> bool:
    """Check to see if the trip is a `prior month` trip."""
    for line in parsed_trip.parsed_lines:
        if "trip_header" == line.id:
            if "prior" in line.indexed_string.txt:
                return True
    return False
