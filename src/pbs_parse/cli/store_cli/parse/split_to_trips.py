"""FILE: split_to_trips.py."""

from rich.progress import TaskID

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
from pbs_parse.pbs_2022_01.split.extract_trips import parse_trip_lines_from_file

from .progress import progress


def split_to_trips(
    base: str, store: StoreManager, task_id: TaskID, overwrite: bool = False
):
    """Split pages to trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    page_infos = store.get_files_by_type(
        base=base, file_type=manifest.FileTypes.SPLIT_PAGE
    )
    progress.update(
        task_id=task_id, total=len(page_infos), description="Splitting pages...."
    )
    count = 0
    for page_info in page_infos:
        path_in = store.manifest_directory / page_info["file_path"]
        trips = parse_trip_lines_from_file(path_in=path_in)
        for trip in trips:
            count += 1
            store.save_trip_lines(base=base, trip=trip, overwrite=overwrite)
        progress.update(
            task_id,
            advance=1,
            description=f"Splitting pages to {count} trips.",
        )
