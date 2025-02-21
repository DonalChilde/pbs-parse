"""FILE: expand_trips.py."""

from collections.abc import Iterable, Iterator, Sequence
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_store as STORE
from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip


def expand_trips(
    parsed_trips: Iterable[ParsedTrip],
    task_id: TaskID,
    progress: Progress,
    debug_dir: Path | None = None,
) -> Iterator[ExpandedTrip]:
    """expand_trips.

    Args:
        parsed_trips (Iterable[ParsedTrip]): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
        debug_dir (Path | None, optional): _description_. Defaults to None.

    Yields:
        Iterator[ExpandedTrip]: _description_
    """
    with_errors = 0
    total_errors = 0
    for idx, expanded_trip in enumerate(
        API.transform.parsed_to_expanded(
            parsed_trips=parsed_trips, debug_dir=debug_dir
        ),
        start=1,
    ):
        if expanded_trip.errors:
            with_errors += 1
            total_errors += len(expanded_trip.errors)
        error_msg = f"{f'[red]{with_errors} expanded trips with errors, {total_errors} errors total.' if with_errors else ''}"
        progress.update(
            task_id,
            completed=idx,
            description=f"Expanding Trips.... {error_msg}",
        )
        yield expanded_trip


def expand_trips_store(
    base_name: str,
    store: STORE.StoreManager,
    task_id: TaskID,
    progress: Progress,
    overwrite: bool = False,
):
    """expand_trips_store.

    Args:
        base_name (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    parsed_trips = list(STORE.load.all_parsed_trips(store=store, base_name=base_name))
    progress.update(
        task_id=task_id, total=len(parsed_trips), description="Expanding Trips...."
    )

    for e_trip in expand_trips(
        parsed_trips=parsed_trips,
        task_id=task_id,
        progress=progress,
    ):
        STORE.save.expanded_trip(
            store=store, base_name=base_name, expanded=e_trip, overwrite=overwrite
        )


def expand_trips_disk(
    parsed_paths: Sequence[Path],
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
    debug_dir: Path | None,
):
    """expand_trips_disk.

    Args:
        parsed_paths (Sequence[Path]): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
        debug_dir (Path | None): _description_
    """
    parsed_trips = (API.load.parsed_trip(file_in=x) for x in parsed_paths)
    progress.update(
        task_id=task_id,
        total=len(parsed_paths),
        description="Expanding Trips....",
    )
    for e_trip in expand_trips(
        parsed_trips=parsed_trips,
        task_id=task_id,
        progress=progress,
        debug_dir=debug_dir,
    ):
        API.save.expanded_trip(
            dir_out=path_out, expanded_trip=e_trip, overwrite=overwrite
        )
