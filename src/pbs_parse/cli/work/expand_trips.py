"""FILE: expand_trips.py."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse.cli.work.common import KeyedResource
from pbs_parse.pbs_2022_01.expand_from_parsed.parsed_to_expanded import ParsedToExpanded
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip, ExpandedTripSaver
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.snippets.file.data_file_loader import FileResource


def expand_trips(
    parsed_trips: Iterable[KeyedResource[ParsedTrip]],
    task_id: TaskID,
    progress: Progress,
) -> Iterator[ExpandedTrip]:
    """expand_trips.

    Args:
        parsed_trips (Iterable[KeyedResource[ParsedTrip]]): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[ExpandedTrip]: _description_
    """
    trips_found = 0
    with_errors = 0
    total_errors = 0
    for idx, parsed in enumerate(parsed_trips, start=1):
        expander = ParsedToExpanded(parsed_trip=parsed.resource, source_file=parsed.key)
        for expanded_trip in expander.translate():
            trips_found += 1
            if expanded_trip.errors:
                with_errors += 1
                total_errors += len(expanded_trip.errors)
            error_msg = f"{f'[red]{with_errors} expanded trips with errors, {total_errors} errors total.' if with_errors else ''}"
            progress.update(
                task_id,
                advance=1,
                description=f"Expanding {idx} trips to {trips_found} trips. {error_msg}",
            )
            yield expanded_trip


def expand_trips_store(
    base: str,
    store: STORE.StoreManager,
    task_id: TaskID,
    progress: Progress,
    overwrite: bool = False,
):
    """expand_trips_store.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    trip_infos = store.get_file_info_by_type(
        base=base, file_type=manifest.FileTypes.PARSED_TRIP
    )
    progress.update(
        task_id=task_id, total=len(trip_infos), description="Expanding trips...."
    )
    parsed_trips = (
        KeyedResource[ParsedTrip](
            resource=STORE.load.parsed_trip(store=store, base=base, key=x["key"]),
            key=x["key"],
        )
        for x in trip_infos
    )
    for e_trip in expand_trips(
        parsed_trips=parsed_trips,
        task_id=task_id,
        progress=progress,
    ):
        STORE.save.expanded_trip(
            store=store, base=base, expanded=e_trip, overwrite=overwrite
        )


def expand_trips_disk(
    parsed_resources: Iterable[FileResource[ParsedTrip]],
    parsed_count: int,
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """expand_trips_disk.

    Args:
        parsed_resources (Iterable[FileResource[ParsedTrip]]): _description_
        parsed_count (int): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    parsed_trips = (
        KeyedResource[ParsedTrip](resource=x.resource, key=x.file_path.name)
        for x in parsed_resources
    )
    progress.update(
        task_id=task_id,
        total=parsed_count,
        description="Expanding trips....",
    )
    saver = ExpandedTripSaver(path_out=path_out)
    for e_trip in expand_trips(
        parsed_trips=parsed_trips, task_id=task_id, progress=progress
    ):
        saver(expanded_trip=e_trip, overwrite=overwrite)
