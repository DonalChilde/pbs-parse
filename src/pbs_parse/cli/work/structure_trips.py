"""FILE: structure_trips.py."""

from collections.abc import Iterable, Iterator
from datetime import date
from pathlib import Path

from rich.progress import Progress, TaskID

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip, ParsedTripLoader
from pbs_parse.pbs_2022_01.models.structured import StructuredTrip, StructuredTripSaver
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
from pbs_parse.pbs_2022_01.structure.parsed_to_structured import (
    structure_trip,
)


def structure_trips(
    parsed_trips: Iterable[ParsedTrip],
    effective_from: date,
    effective_to: date,
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
        s_trip = structure_trip(
            parsed_trip=trip, effective_from=effective_from, effective_to=effective_to
        )
        trips_structured += 1
        progress.update(
            task_id,
            advance=1,
        )
        yield s_trip


def structure_trips_store(
    base: str,
    store: StoreManager,
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
    effective_from, effective_to = store.get_effective_dates()
    structured_trips = structure_trips(
        parsed_trips=store.load_all_parsed_trips(base=base),
        effective_from=effective_from,
        effective_to=effective_to,
        task_id=task_id,
        progress=progress,
    )
    for structured_trip in structured_trips:
        store.save_structured_trip(
            base=base, structured=structured_trip, overwrite=overwrite
        )


def structure_trips_disk(
    path_in: Path,
    path_out: Path,
    overwrite: bool,
    effective_from: date,
    effective_to: date,
    task_id: TaskID,
    progress: Progress,
):
    """structure_trips_disk.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        effective_from (date): _description_
        effective_to (date): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    loader = ParsedTripLoader(path_in=path_in)
    parsed_trips = (x.resource for x in loader())
    progress.update(
        task_id=task_id,
        total=loader.file_count,
        description="Structuring trips....",
    )
    saver = StructuredTripSaver(path_out=path_out)
    structured_trips = structure_trips(
        parsed_trips=parsed_trips,
        effective_from=effective_from,
        effective_to=effective_to,
        task_id=task_id,
        progress=progress,
    )
    for structured_trip in structured_trips:
        saver(structured_trip=structured_trip, overwrite=overwrite)
