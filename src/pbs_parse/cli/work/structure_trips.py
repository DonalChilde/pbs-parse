"""FILE: structure_trips.py."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse.cli.work.common import KeyedResource
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.structured import StructuredTrip, StructuredTripSaver
from pbs_parse.pbs_2022_01.structure.parsed_to_structured import (
    structure_trip,
)
from pbs_parse.snippets.file.data_file_loader import FileResource


def structure_trips(
    parsed_trips: Iterable[KeyedResource[ParsedTrip]],
    task_id: TaskID,
    progress: Progress,
) -> Iterator[StructuredTrip]:
    """structure_trips.

    Args:
        parsed_trips (Iterable[ParsedTrip]): _description_
        effective_from (date): _description_
        effective_to (date): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[StructuredTrip]: _description_
    """
    trips_structured = 0
    for trip in parsed_trips:
        s_trip = structure_trip(parsed_trip=trip.resource, source_file=trip.key)
        trips_structured += 1
        progress.update(
            task_id,
            advance=1,
        )
        yield s_trip


def structure_trips_store(
    base: str,
    store: STORE.StoreManager,
    task_id: TaskID,
    progress: Progress,
    overwrite: bool = False,
):
    """structure_trips_store.

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
    total_trips = len(trip_infos)
    progress.update(
        task_id=task_id, total=total_trips, description="Structuring trips...."
    )
    parsed_trips = (
        KeyedResource[ParsedTrip](
            resource=STORE.load.parsed_trip(store=store, base=base, key=x["key"]),
            key=x["key"],
        )
        for x in trip_infos
    )
    structured_trips = structure_trips(
        parsed_trips=parsed_trips,
        task_id=task_id,
        progress=progress,
    )
    for structured_trip in structured_trips:
        STORE.save.structured_trip(
            store=store, base=base, structured=structured_trip, overwrite=overwrite
        )


def structure_trips_disk(
    parsed_resources: Iterable[FileResource[ParsedTrip]],
    parsed_count: int,
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """structure_trips_disk.

    Args:
        parsed_resources (Iterable[FileResource[ParsedTrip]]): _description_
        parsed_count (int): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        effective_from (date): _description_
        effective_to (date): _description_
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
        description="Structuring trips....",
    )
    saver = StructuredTripSaver(path_out=path_out)
    structured_trips = structure_trips(
        parsed_trips=parsed_trips,
        task_id=task_id,
        progress=progress,
    )
    for structured_trip in structured_trips:
        saver(structured_trip=structured_trip, overwrite=overwrite)
