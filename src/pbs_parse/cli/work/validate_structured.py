"""FILE: validate_structured.py."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.structured import StructuredTrip
from pbs_parse.pbs_2022_01.models.structured_validation import (
    STRUCTURED_VALIDATION_SERIALIZER,
    StructuredValidation,
)
from pbs_parse.pbs_2022_01.structure.validate.validate_structured_trip import (
    validate_structured_trip,
)
from pbs_parse.pbs_2022_01.structure.validate.validation_model_factories import (
    validation_model_from_objects,
)
from pbs_parse.snippets.file.data_file_loader import FileResource

from .common import load_parsed


def validate_structured(
    vms: Iterable[StructuredValidation],
    task_id: TaskID,
    progress: Progress,
) -> Iterator[StructuredValidation]:
    """validate_structured.

    Args:
        vms (Iterable[StructuredValidation]): Validation models.
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[StructuredValidation]: _description_
    """
    errors_found = 0
    errors_found_detailed = 0
    for vm in vms:
        validate_structured_trip(vm=vm)
        if vm.errors:
            errors_found += 1
            errors_found_detailed += len(vm.errors)
            progress.update(
                task_id,
                advance=1,
                description=f"{f"[red]{errors_found} structured trips with errors, {errors_found_detailed} errors total." if errors_found else None}",
            )
        else:
            progress.update(task_id=task_id, advance=1)
        yield vm


def validate_structured_store(
    base: str,
    store: STORE.StoreManager,
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
    structured_infos = store.get_file_info_by_type(
        base=base, file_type=manifest.FileTypes.STRUCTURED_TRIP
    )
    total_trips = len(structured_infos)
    progress.update(
        task_id=task_id,
        total=total_trips,
        description="Validating structured trips....",
    )
    structured_trips = (
        STORE.load.structured_trip(store=store, base=base, uuid=x["key"])
        for x in structured_infos
    )
    validation_models = (
        validation_model_from_objects(
            parsed_trip=STORE.load.parsed_trip(
                store=store, base=base, uuid=x.source_uuid
            ),
            structured_trip=x,
            parsed_trip_path="",
            structured_trip_path="",
        )
        for x in structured_trips
    )
    for sv in validate_structured(
        vms=validation_models, task_id=task_id, progress=progress
    ):
        if sv.errors:
            STORE.save.structured_trip_validation_error(
                store=store, base=base, validation_model=sv, overwrite=overwrite
            )


def validate_structured_disk(
    structured_resources: Iterable[FileResource[StructuredTrip]],
    structured_count: int,
    parsed_dir: Path,
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """validate_structured_disk.

    Args:
        structured_resources (Iterable[FileResource[StructuredTrip]]): _description_
        structured_count (int): _description_
        parsed_dir (Path): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    progress.update(
        task_id=task_id,
        total=structured_count,
        description="Validating structured trips....",
    )
    validation_models = generate_validation_models(
        resources=structured_resources, parsed_dir=parsed_dir
    )
    for sv in validate_structured(
        vms=validation_models, task_id=task_id, progress=progress
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
        vm = validation_model_from_objects(
            parsed_trip=parsed_resource.resource,
            parsed_trip_path=str(parsed_resource.file_path),
            structured_trip=s_trip_res.resource,
            structured_trip_path=str(s_trip_res.file_path),
        )
        yield vm
