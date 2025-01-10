"""FILE: split_to_pages.py."""

from collections.abc import Iterator
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.page_lines import PageLines, PageLinesSaver
from pbs_parse.pbs_2022_01.split.extract_pages import parse_page_lines_from_file


def split_to_pages(
    path_in: Path, task_id: TaskID, progress: Progress
) -> Iterator[PageLines]:
    """split_to_pages.

    Args:
        path_in (Path): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[PageLines]: _description_
    """
    pages_found = 0
    pages = parse_page_lines_from_file(path_in=path_in)
    for page in pages:
        pages_found += 1
        progress.update(
            task_id=task_id,
            description=f"Splitting package to {pages_found} pages.",
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
    source_path = source_info[0]["file_path"]
    progress.update(task_id=task_id, total=1, description="Splitting package....")
    path_in = store.manifest_directory / source_path
    for page in split_to_pages(path_in=path_in, task_id=task_id, progress=progress):
        STORE.save.page_lines(store=store, base=base, page=page, overwrite=overwrite)
    progress.update(task_id=task_id, advance=1)


def split_to_pages_disk(
    path_in: Path, path_out: Path, overwrite: bool, task_id: TaskID, progress: Progress
):
    """split_to_pages_disk.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    progress.update(task_id=task_id, total=1, description="Splitting package....")
    pages = split_to_pages(path_in=path_in, task_id=task_id, progress=progress)
    page_saver = PageLinesSaver(path_out=path_out)
    for page in pages:
        page_saver(page_lines=page, overwrite=overwrite)
    progress.update(task_id=task_id, advance=1)
