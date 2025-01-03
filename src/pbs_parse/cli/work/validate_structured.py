"""FILE: validate_structured.py."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from rich.progress import Progress, TaskID

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.structured import StructuredTrip, StructuredTripLoader
from pbs_parse.pbs_2022_01.models.structured_validation import (
    STRUCTURED_VALIDATION_SERIALIZER,
    StructuredValidation,
)
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
from pbs_parse.pbs_2022_01.validate.validate_structured import StructuredValidator
from pbs_parse.snippets.file.data_file_loader import FileResource

from .common import load_parsed


def validate_structured(
    validation_models: Iterable[StructuredValidation],
    task_id: TaskID,
    progress: Progress,
) -> Iterator[StructuredValidation]:
    """validate_structured.

    Args:
        validation_models (Iterable[StructuredValidation]): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[StructuredValidation]: _description_
    """
    errors_found = 0
    errors_found_detailed = 0
    validator = StructuredValidator()
    for sv in validation_models:
        validator.validate(validation_model=sv)
        if sv.errors:
            errors_found += 1
            errors_found_detailed += len(sv.errors)
            progress.update(
                task_id,
                advance=1,
                description=f"{f"[red]{errors_found} structured trips with errors, {errors_found_detailed} errors total." if errors_found else None}",
            )
        else:
            progress.update(task_id=task_id, advance=1)
        yield sv


def validate_structured_store(
    base: str,
    store: StoreManager,
    task_id: TaskID,
    progress: Progress,
    overwrite: bool = False,
):
    """validate_structured_store.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    total_trips = len(
        store.get_file_info_by_type(
            base=base, file_type=manifest.FileTypes.STRUCTURED_TRIP
        )
    )
    progress.update(
        task_id=task_id,
        total=total_trips,
        description="Validating structured trips....",
    )
    structured_trips = store.load_all_structured_trips(base=base)
    validation_models = (
        StructuredValidation(
            parsed=store.load_parsed_trip(base=base, uuid=x.uuid),
            structured=x,
            parsed_path="",
            structured_path="",
        )
        for x in structured_trips
    )
    for sv in validate_structured(
        validation_models=validation_models, task_id=task_id, progress=progress
    ):
        if sv.errors:
            store.save_structured_trip_validation_error(
                base=base, validation_model=sv, overwrite=overwrite
            )


def validate_structured_disk(
    path_in: Path,
    parsed_dir: Path,
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """validate_structured_disk.

    Args:
        path_in (Path): _description_
        parsed_dir (Path): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    loader = StructuredTripLoader(path_in=path_in)
    resources = loader()
    progress.update(
        task_id=task_id,
        total=loader.file_count,
        description="Validating structured trips....",
    )
    validation_models = generate_validation_models(
        resources=resources, parsed_dir=parsed_dir
    )
    for sv in validate_structured(
        validation_models=validation_models, task_id=task_id, progress=progress
    ):
        if sv.errors:
            file_out = path_out / sv.default_file_name()
            STRUCTURED_VALIDATION_SERIALIZER.save_as_json(
                path_out=file_out, complex_obj=sv, overwrite=overwrite
            )
            txt_out = file_out.with_suffix(".txt")
            txt_out.write_text(str(sv))


def generate_validation_models(
    resources: Iterable[FileResource[StructuredTrip]], parsed_dir: Path
) -> Iterable[StructuredValidation]:
    """generate_validation_models.

    Args:
        resources (Iterable[FileResource[StructuredTrip]]): _description_
        parsed_dir (Path): _description_

    Returns:
        Iterable[StructuredValidation]: _description_

    Yields:
        Iterator[Iterable[StructuredValidation]]: _description_
    """
    for s_trip_res in resources:
        parsed_resource = load_parsed(parsed_dir=parsed_dir, s_trip=s_trip_res.resource)
        sv = StructuredValidation(
            parsed=parsed_resource.resource,
            parsed_path=str(parsed_resource.file_path),
            structured=s_trip_res.resource,
            structured_path=str(s_trip_res.file_path),
        )
        yield sv
