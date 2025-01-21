"""FILE: validate_expanded.py."""

from collections.abc import Iterable, Iterator
from pathlib import Path

from rich.progress import Progress, TaskID

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse.cli.work.common import load_parsed, load_structured
from pbs_parse.pbs_2022_01.expand.validate.validate_expanded_trip import (
    validate_expanded_trip,
)
from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.expanded_validation import (
    EXPANDED_VALIDATION_SERIALIZER,
    ExpandedValidation,
)
from pbs_parse.snippets.file.data_file_loader import FileResource


def validate_expanded(
    validation_models: Iterable[ExpandedValidation],
    task_id: TaskID,
    progress: Progress,
) -> Iterator[ExpandedValidation]:
    """validate_expanded.

    Args:
        validation_models (Iterable[ExpandedValidation]): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_

    Yields:
        Iterator[ExpandedValidation]: _description_
    """
    errors_found = 0
    errors_found_detailed = 0
    for vm in validation_models:
        validate_expanded_trip(vm=vm)
        if vm.expanded.errors:
            errors_found += 1
            errors_found_detailed += len(vm.expanded.errors)
            progress.update(
                task_id,
                advance=1,
                description=f"{f'[red]{errors_found} expanded trips with errors, {errors_found_detailed} errors total.' if errors_found else None}",
            )
        else:
            progress.update(task_id=task_id, advance=1)
        yield vm


def validate_expanded_store(
    base: str,
    store: STORE.StoreManager,
    task_id: TaskID,
    progress: Progress,
    overwrite: bool = False,
):
    """validate_expanded_store.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    expanded_infos = store.get_file_info_by_type(
        base=base, file_type=manifest.FileTypes.EXPANDED_TRIP
    )
    total_trips = len(expanded_infos)
    progress.update(
        task_id=task_id,
        total=total_trips,
        description="Validating expanded trips....",
    )
    expanded_trips = (
        STORE.load.expanded_trip(store=store, base=base, key=x["key"])
        for x in expanded_infos
    )
    validation_models = (
        ExpandedValidation(
            expanded=x,
            structured=STORE.load.structured_trip(
                store=store, base=base, key=x.source.structured_trip
            ),
        )
        for x in expanded_trips
    )
    for vm in validate_expanded(
        validation_models=validation_models, task_id=task_id, progress=progress
    ):
        if vm.expanded.errors:
            vm.parsed = STORE.load.parsed_trip(
                store=store, base=base, key=vm.expanded.source.parsed_trip
            )
            STORE.save.expanded_trip_validation_error(
                store=store, base=base, validation_model=vm, overwrite=overwrite
            )


def validate_expanded_disk(
    expanded_resources: Iterable[FileResource[ExpandedTrip]],
    expanded_count: int,
    structured_dir: Path,
    parsed_dir: Path,
    path_out: Path,
    overwrite: bool,
    task_id: TaskID,
    progress: Progress,
):
    """validate_expanded_disk.

    Args:
        expanded_resources (Iterable[FileResource[ExpandedTrip]]): _description_
        expanded_count (int): _description_
        structured_dir (Path): _description_
        parsed_dir (Path): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
        task_id (TaskID): _description_
        progress (Progress): _description_
    """
    progress.update(
        task_id=task_id,
        total=expanded_count,
        description="Validating expanded trips....",
    )
    validation_models = generate_validation_models(
        resources=expanded_resources, structured_dir=structured_dir
    )
    for vm in validate_expanded(
        validation_models=validation_models, task_id=task_id, progress=progress
    ):
        if vm.expanded.errors:
            parsed = load_parsed(parsed_dir=parsed_dir, s_trip=vm.structured)
            vm.parsed = parsed.resource
            vm.parsed_path = str(parsed.file_path)
            file_out = path_out / vm.default_file_name()
            EXPANDED_VALIDATION_SERIALIZER.save_as_json(
                path_out=file_out, complex_obj=vm, overwrite=overwrite
            )
            txt_out = file_out.with_suffix(".txt")
            txt_out.write_text(str(vm))


def generate_validation_models(
    resources: Iterable[FileResource[ExpandedTrip]], structured_dir: Path
) -> Iterable[ExpandedValidation]:
    """generate_validation_models.

    Args:
        resources (Iterable[FileResource[ExpandedTrip]]): _description_
        structured_dir (Path): _description_

    Returns:
        Iterable[ExpandedValidation]: _description_

    Yields:
        Iterator[Iterable[ExpandedValidation]]: _description_
    """
    for e_trip_res in resources:
        structured_resource = load_structured(
            structured_dir=structured_dir, e_trip=e_trip_res.resource
        )
        vm = ExpandedValidation(
            expanded=e_trip_res.resource,
            expanded_path=str(e_trip_res.file_path),
            structured=structured_resource.resource,
            structured_path=str(e_trip_res.file_path),
        )
        yield vm
