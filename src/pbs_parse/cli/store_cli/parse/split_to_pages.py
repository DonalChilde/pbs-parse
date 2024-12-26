"""FILE: split_to_pages.py."""

from rich.progress import TaskID

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
from pbs_parse.pbs_2022_01.split.extract_pages import parse_page_lines_from_file

from .progress import progress


def split_to_pages(base: str, store: StoreManager, task_id: TaskID):
    """split_to_pages _summary_.

    Code to split pages, with rich progress.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    source_info = store.get_files_by_type(
        base=base, file_type=manifest.FileTypes.TXT_PACKAGE
    )
    source_path = source_info[0]["file_path"]
    progress.update(task_id=task_id, total=1, description="Splitting pages....")
    msg = f"Splitting pages from {source_path}"
    progress.console.print(msg)
    path_in = store.manifest_path / source_info[0]["file_path"]
    pages = parse_page_lines_from_file(path_in=path_in)
    count = store.save_page_lines(base=base, pages=pages)
    progress.update(
        task_id=task_id, completed=True, description=f"Found {count} pages."
    )
    msg = f"Found {count} pages in {source_path}"
    progress.console.print(msg)
