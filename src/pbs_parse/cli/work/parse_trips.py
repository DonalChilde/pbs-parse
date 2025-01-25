"""FILE: parse_trips.py."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from pfmsoft.state_parser import ParseContext
from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse.cli.work.common import KeyedResource
from pbs_parse.common.is_prior_month import is_prior_month
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip, ParsedTripSaver
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines
from pbs_parse.pbs_2022_01.parse.trip_lines_parser import TripLinesParser
from pbs_parse.snippets.file.data_file_loader import FileResource


def parse_trips(
    trip_lines: Iterable[KeyedResource[TripLines]],
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
    prior_trips = 0
    parser = TripLinesParser()
    for trip in trip_lines:
        ctx = ParseContext()
        parsed_trip = parser.parse(ctx=ctx, trip_lines=trip.resource, source=trip.key)
        trips_parsed += 1
        if is_prior_month(parsed_trip=parsed_trip):
            prior_trips += 1
        progress.update(
            task_id,
            advance=1,
            description=f"Parsing trips..... {prior_trips} prior month trips found.",
        )
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
        task_id=task_id, total=len(trip_infos), description="Parsing trips...."
    )
    trip_lines = (
        KeyedResource[TripLines](
            resource=STORE.load.trip_lines(store=store, base=base, key=x["key"]),
            key=x["key"],
        )
        for x in trip_infos
    )
    for parsed_trip in parse_trips(
        trip_lines=trip_lines,
        task_id=task_id,
        progress=progress,
    ):
        if is_prior_month(parsed_trip=parsed_trip):
            STORE.save.parsed_prior_month_trip(
                store=store, base=base, parsed=parsed_trip, overwrite=overwrite
            )
        else:
            STORE.save.parsed_trip(
                store=store, base=base, parsed=parsed_trip, overwrite=overwrite
            )


def parse_trips_disk(
    trip_resources: Iterable[FileResource[TripLines]],
    trip_count: int,
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """parse_trips_disk.

    Args:
        trip_resources (Iterable[FileResource[TripLines]]): _description_
        trip_count (int): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    # loader = TripLinesLoader(path_in=path_in)
    trip_lines = (
        KeyedResource[TripLines](resource=x.resource, key=x.file_path.name)
        for x in trip_resources
    )
    progress.update(task_id=task_id, total=trip_count, description="Parsing trips....")
    saver = ParsedTripSaver(path_out=path_out)
    prior_saver = ParsedTripSaver(path_out=path_out / "prior")
    for parsed_trip in parse_trips(
        trip_lines=trip_lines, task_id=task_id, progress=progress
    ):
        if is_prior_month(parsed_trip=parsed_trip):
            prior_saver(parsed_trip=parsed_trip, overwrite=overwrite)
        else:
            saver(parsed_trip=parsed_trip, overwrite=overwrite)
