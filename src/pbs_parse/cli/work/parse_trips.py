"""FILE: parse_trips.py."""

from collections.abc import Iterable, Iterator, Sequence
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_store as STORE
from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines


def parse_trips(
    trip_lines: Iterable[TripLines],
    task_id: TaskID,
    progress: Progress,
) -> Iterator[ParsedTrip]:
    """parse_trips.

    Args:
        trip_lines (Iterable[TripLines]): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[ParsedTrip]: _description_
    """
    trips_parsed = 0

    for parsed_trip in API.transform.trips_to_parsed(trips=trip_lines):
        trips_parsed += 1
        progress.update(task_id, advance=1)
        yield parsed_trip


def parse_trips_store(
    base: str,
    store: STORE.StoreManager,
    task_id: TaskID,
    progress: Progress,
    overwrite: bool = False,
):
    """parse_trips_store.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    trip_infos = store.get_file_info_by_type(
        base=base, file_type=manifest.FileTypes.SPLIT_TRIP
    )
    progress.update(
        task_id=task_id, total=len(trip_infos), description="Parsing Trips...."
    )
    trip_lines = (
        STORE.load.trip_lines(store=store, base=base, key=x["key"]) for x in trip_infos
    )
    for parsed_trip in parse_trips(
        trip_lines=trip_lines,
        task_id=task_id,
        progress=progress,
    ):
        STORE.save.parsed_trip(
            store=store, base=base, parsed=parsed_trip, overwrite=overwrite
        )


def parse_trips_disk(
    trip_paths: Sequence[Path],
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """parse_trips_disk.

    Args:
        trip_paths (Sequence[Path]): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    trip_lines = (API.load.trip_lines(file_in=x) for x in trip_paths)
    progress.update(
        task_id=task_id, total=len(trip_paths), description="Parsing Trips...."
    )

    for parsed_trip in parse_trips(
        trip_lines=trip_lines, task_id=task_id, progress=progress
    ):
        API.save.parsed_trip(
            dir_out=path_out, parsed_trip=parsed_trip, overwrite=overwrite
        )
