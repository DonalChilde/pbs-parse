"""FILE: validate_expanded_trips.py."""

from rich.progress import TaskID

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.expanded_validation import ExpandedValidation
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
from pbs_parse.pbs_2022_01.validate.validate_expanded import validate_expanded

from .progress import progress


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
    total_trips = len(expanded_trips)
    errors = 0
    progress.update(
        task_id=task_id,
        total=total_trips,
        description="Validating expanded trips....",
    )
    for trip_info in expanded_trips:
        expanded = store.load_expanded_trip(base=base, uuid=trip_info["key"])
        structured = store.load_structured_trip(base=base, uuid=expanded.source_uuid)
        validation_model = ExpandedValidation(expanded=expanded, structured=structured)
        validate_expanded(validation_model=validation_model)
        if validation_model.errors:
            parsed = store.load_parsed_trip(base=base, uuid=structured.source_uuid)
            validation_model.parsed = parsed
            store.save_expanded_trip_validation_error(
                base=base, validation_model=validation_model
            )
            errors += 1
        progress.update(
            task_id,
            advance=1,
            description=f"{"[red]" if errors else ""}Validating expanded trips, {errors} errors.",
        )
