"""FILE: validate_expanded_trips.py."""

from rich.progress import TaskID

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager


def validate_expanded_trips(base: str, store: StoreManager, task_id: TaskID):
    """validate_expanded_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    expanded_trips = store.get_file_info_by_type(
        base=base, file_type=manifest.FileTypes.EXPANDED_TRIP
    )
    for trip_info in expanded_trips:
        expanded = store.load_expanded_trip(base=base, uuid=trip_info["key"])
        structured = store.load_structured_trip(base=base, uuid=expanded.source_uuid)
        parsed = store.load_parsed_trip(base=base, uuid=structured.source_uuid)
