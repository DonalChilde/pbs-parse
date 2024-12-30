"""FILE: split_to_pages.py."""

from rich.progress import TaskID

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
from pbs_parse.pbs_2022_01.split.extract_pages import parse_page_lines_from_file

from .progress import progress


def split_to_pages(
    base: str, store: StoreManager, task_id: TaskID, overwrite: bool = False
):
    """Split a text bid package to pages.

    Code to split pages, with rich progress.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    source_info = store.get_files_by_type(
        base=base, file_type=manifest.FileTypes.TXT_PACKAGE
    )
    source_path = source_info[0]["file_path"]
    progress.update(task_id=task_id, total=0, description="Splitting package....")
    path_in = store.manifest_directory / source_path
    pages = parse_page_lines_from_file(path_in=path_in)
    count = 0
    for page in pages:
        store.save_page_lines(base=base, page=page, overwrite=overwrite)
        count += 1
        progress.update(
            task_id=task_id,
            advance=1,
            completed=True,
            description=f"Splitting package to {count} pages.",
        )
