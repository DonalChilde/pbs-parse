"""FILE: structure_trips.py."""

from rich.progress import TaskID

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
from pbs_parse.pbs_2022_01.structure.parsed_to_structured import (
    structure_trip_from_file,
)

from .progress import progress


def structure_trips(
    base: str, store: StoreManager, task_id: TaskID, overwrite: bool = False
):
    """structure_trips _summary_.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
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
    for trip in trip_infos:
        path_in = store.manifest_directory / trip["file_path"]
        structured_trip = structure_trip_from_file(
            path_in=path_in, effective_from=effective_from, effective_to=effective_to
        )
        store.save_structured_trip(
            base=base, structured=structured_trip, overwrite=overwrite
        )
        progress.update(
            task_id,
            advance=1,
            # description=f"{idx} of {total_trips} trips structured.",
        )
