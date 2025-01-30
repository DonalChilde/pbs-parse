"""FILE: split_to_pages.py."""

from collections.abc import Iterator
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.bid_data import BidData, Effective
from pbs_parse.pbs_2022_01.models.page_lines import PageLines


def split_to_pages(
    path_in: Path, bid: BidData, task_id: TaskID, progress: Progress
) -> Iterator[PageLines]:
    """split_to_pages.

    Args:
        path_in (Path): _description_
        bid (BidData): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[PageLines]: _description_
    """
    for idx, page in enumerate(
        API.transform.source_to_pages(path_in=path_in, bid=bid), start=1
    ):
        progress.update(
            task_id=task_id,
            completed=idx,
        )
        yield page


def split_to_pages_store(
    base: str,
    store: STORE.StoreManager,
    task_id: TaskID,
    progress: Progress,
    overwrite: bool = False,
):
    """split_to_pages_store.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    source_info = store.get_file_info_by_type(
        base=base, file_type=manifest.FileTypes.TXT_PACKAGE
    )
    effective_from, effective_to = STORE.get.effective_dates(store=store)
    name = STORE.get.name(store=store)
    source_path = source_info[0]["file_path"]
    bid = BidData(
        name=name,
        base=base,
        effective=Effective(start=effective_from, end=effective_to),
    )
    progress.update(task_id=task_id, total=1, description="Splitting package....")
    path_in = store.manifest_directory / source_path
    for idx, page in enumerate(
        split_to_pages(path_in=path_in, bid=bid, task_id=task_id, progress=progress),
        start=1,
    ):
        STORE.save.page_lines(store=store, base=base, page=page, overwrite=overwrite)
        progress.update(task_id=task_id, completed=idx)


def split_to_pages_disk(
    path_in: Path,
    path_out: Path,
    bid: BidData,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """split_to_pages_disk.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        bid (BidData): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    progress.update(task_id=task_id, total=1, description="Splitting package....")
    pages = split_to_pages(path_in=path_in, bid=bid, task_id=task_id, progress=progress)
    for page in pages:
        API.save.page_lines(dir_out=path_out, page_lines=page, overwrite=overwrite)
