"""FILE: expand_trips.py."""

from rich.progress import TaskID

from pbs_parse.pbs_2022_01.expand.structured_to_expanded_cls import StructuredToExpanded
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

from .progress import progress


def expand_trips(
    base: str, store: StoreManager, task_id: TaskID, overwrite: bool = False
):
    """expand_trips .

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    trip_infos = store.get_file_info_by_type(
        base=base, file_type=manifest.FileTypes.STRUCTURED_TRIP
    )
    total_trips = len(trip_infos)
    progress.update(
        task_id=task_id, total=total_trips, description="Expanding trips...."
    )
    trips_found = 0
    for trip in trip_infos:
        path_in = store.manifest_directory / trip["file_path"]
        expander = StructuredToExpanded.from_file(path_in=path_in)
        for expanded in expander.translate():
            trips_found += 1
            store.save_expanded_trip(base=base, expanded=expanded, overwrite=overwrite)
        progress.update(
            task_id,
            advance=1,
            description=f"Expanding trips to {trips_found} trips.",
        )
