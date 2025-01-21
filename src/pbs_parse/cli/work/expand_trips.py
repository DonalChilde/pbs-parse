"""FILE: expand_trips.py."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse.cli.work.common import KeyedResource
from pbs_parse.pbs_2022_01.expand.structured_to_expanded import StructuredToExpanded
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip, ExpandedTripSaver
from pbs_parse.pbs_2022_01.models.structured import StructuredTrip
from pbs_parse.snippets.file.data_file_loader import FileResource


def expand_trips(
    structured_trips: Iterable[KeyedResource[StructuredTrip]],
    task_id: TaskID,
    progress: Progress,
) -> Iterator[ExpandedTrip]:
    """expand_trips.

    Args:
        structured_trips (Iterable[StructuredTrip]): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[ExpandedTrip]: _description_
    """
    trips_found = 0
    for idx, s_trip in enumerate(structured_trips, start=1):
        expander = StructuredToExpanded(
            structured_trip=s_trip.resource, source_file=s_trip.key
        )
        for e_trip in expander.translate():
            trips_found += 1
            progress.update(
                task_id,
                advance=1,
                description=f"Expanding {idx} trips to {trips_found} trips.",
            )
            yield e_trip


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
        base=base, file_type=manifest.FileTypes.STRUCTURED_TRIP
    )
    progress.update(
        task_id=task_id, total=len(trip_infos), description="Expanding trips...."
    )
    structured_trips = (
        KeyedResource[StructuredTrip](
            resource=STORE.load.structured_trip(store=store, base=base, key=x["key"]),
            key=x["key"],
        )
        for x in trip_infos
    )
    for e_trip in expand_trips(
        structured_trips=structured_trips,
        task_id=task_id,
        progress=progress,
    ):
        STORE.save.expanded_trip(
            store=store, base=base, expanded=e_trip, overwrite=overwrite
        )


def expand_trips_disk(
    structured_resources: Iterable[FileResource[StructuredTrip]],
    structured_count: int,
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """expand_trips_disk.

    Args:
        structured_resources (Iterable[FileResource[StructuredTrip]]): _description_
        structured_count (int): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    s_trips = (
        KeyedResource[StructuredTrip](resource=x.resource, key=x.file_path.name)
        for x in structured_resources
    )
    progress.update(
        task_id=task_id,
        total=structured_count,
        description="Expanding trips....",
    )
    saver = ExpandedTripSaver(path_out=path_out)
    for e_trip in expand_trips(
        structured_trips=s_trips, task_id=task_id, progress=progress
    ):
        saver(expanded_trip=e_trip, overwrite=overwrite)
