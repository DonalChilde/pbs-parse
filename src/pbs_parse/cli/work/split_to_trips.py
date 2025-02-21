"""FILE: split_to_trips.py."""

from collections.abc import Iterable, Iterator, Sequence
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_store as STORE
from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.models.page_lines import PageLines
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines, is_prior_month


def split_to_trips(
    pages: Iterable[PageLines], task_id: TaskID, progress: Progress
) -> Iterator[TripLines]:
    """split_to_trips.

    Args:
        pages (Iterable[PageLines]): _description_
        source_file (str): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[TripLines]: _description_
    """
    prior_trips = 0
    for idx, trip in enumerate(API.transform.pages_to_trips(pages=pages), start=1):
        if is_prior_month(trip):
            prior_trips += 1
        progress.update(
            task_id,
            completed=idx,
            description=f"Splitting Pages to Trips..... {prior_trips} prior month trips found.",
        )
        yield trip


def split_to_trips_store(
    base_name: str,
    store: STORE.StoreManager,
    task_id: TaskID,
    progress: Progress,
    overwrite: bool = False,
):
    """split_to_trips_store.

    Args:
        base_name (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    pages = list(STORE.load.all_pages(store=store, base_name=base_name))
    progress.update(
        task_id=task_id, total=len(pages), description="Splitting pages...."
    )

    for trip in split_to_trips(
        pages=pages,
        task_id=task_id,
        progress=progress,
    ):
        if is_prior_month(trip):
            STORE.save.trip_lines_prior(
                store=store, base_name=base_name, trip=trip, overwrite=overwrite
            )
        else:
            STORE.save.trip_lines(
                store=store, base_name=base_name, trip=trip, overwrite=overwrite
            )


def split_to_trips_disk(
    page_paths: Sequence[Path],
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """split_to_trips_disk.

    Args:
        page_paths (Sequence[Path]): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    pages = (API.load.page_lines(file_in=x) for x in page_paths)
    prior_dir = path_out / "prior"
    for trip in split_to_trips(pages=pages, task_id=task_id, progress=progress):
        if is_prior_month(trip):
            API.save.trip_lines(dir_out=prior_dir, trip_lines=trip, overwrite=overwrite)
        else:
            API.save.trip_lines(dir_out=path_out, trip_lines=trip, overwrite=overwrite)
