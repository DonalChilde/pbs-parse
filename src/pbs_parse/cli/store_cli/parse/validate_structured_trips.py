"""FILE: validate_structure_trips.py."""

from rich.progress import TaskID

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.structured_validation import StructuredValidation
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
from pbs_parse.pbs_2022_01.validate.validate_structured import validate_structured_trip

from .progress import progress


def validate_structured_trips(base: str, store: StoreManager, task_id: TaskID):
    """validate_structured_trips.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
    """
    structured_trips = store.get_file_info_by_type(
        base=base, file_type=manifest.FileTypes.STRUCTURED_TRIP
    )
    total_trips = len(structured_trips)
    errors = 0
    progress.update(
        task_id=task_id,
        total=total_trips,
        description="Validating structured trips....",
    )
    for trip_info in structured_trips:
        structured = store.load_structured_trip(base=base, uuid=trip_info["key"])
        parsed = store.load_parsed_trip(base=base, uuid=structured.source_uuid)
        validation_model = StructuredValidation(
            parsed_trip=parsed,
            structured_trip=structured,
            parsed_path="",
            structured_path="",
        )
        validate_structured_trip(validation_model=validation_model)
        if validation_model.errors:
            store.save_structured_trip_validation_error(
                base=base, validation_model=validation_model, overwrite=False
            )
            errors += 1
        progress.update(
            task_id,
            advance=1,
            description=f"{"[red]" if errors else ""}Validating structured trips, {errors} errors.",
        )
