"""FILE: split_to_trips.py."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.page_lines import PageLines
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines, TripLinesSaver
from pbs_parse.pbs_2022_01.split.extract_trips import parse_trip_lines
from pbs_parse.snippets.file.data_file_loader import FileResource


def split_to_trips(
    pages: Iterable[PageLines], task_id: TaskID, progress: Progress
) -> Iterator[TripLines]:
    """split_to_trips.

    Args:
        pages (Iterable[PageLines]): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[TripLines]: _description_
    """
    trips_found = 0
    for page in pages:
        for trip in parse_trip_lines(page):
            trips_found += 1
            progress.update(
                task_id,
                description=f"Splitting pages to {trips_found} trips.",
            )
            yield trip
        progress.update(task_id=task_id, advance=1)


def split_to_trips_store(
    base: str,
    store: STORE.StoreManager,
    task_id: TaskID,
    progress: Progress,
    overwrite: bool = False,
):
    """split_to_trips_store.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    page_infos = store.get_file_info_by_type(
        base=base, file_type=manifest.FileTypes.SPLIT_PAGE
    )
    progress.update(
        task_id=task_id, total=len(page_infos), description="Splitting pages...."
    )
    pages = (
        STORE.load.page_lines(store=store, base=base, uuid=x["key"]) for x in page_infos
    )
    for trip in split_to_trips(
        pages=pages,
        task_id=task_id,
        progress=progress,
    ):
        STORE.save.trip_lines(store=store, base=base, trip=trip, overwrite=overwrite)


def split_to_trips_disk(
    page_resources: Iterable[FileResource[PageLines]],
    page_count: int,
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """split_to_trips_disk.

    Args:
        page_resources (Iterable[FileResource[PageLines]]): _description_
        page_count (int): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    # page_loader = PageLinesLoader(path_in=path_in)
    pages = (x.resource for x in page_resources)
    progress.update(
        task_id=task_id, total=page_count, description="Splitting pages...."
    )
    trip_saver = TripLinesSaver(path_out=path_out)
    for trip in split_to_trips(pages=pages, task_id=task_id, progress=progress):
        trip_saver(trip_lines=trip, overwrite=overwrite)
