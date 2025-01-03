"""FILE: validate_structured.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.cli.work.common import load_parsed
from pbs_parse.pbs_2022_01.models.structured import STRUCTURED_TRIP_SERIALIZER
from pbs_parse.pbs_2022_01.models.structured_validation import (
    STRUCTURED_VALIDATION_SERIALIZER,
    StructuredValidation,
)
from pbs_parse.pbs_2022_01.validate.validate_structured import StructuredValidator

from ..work.progress import progress
from ..work.validate_structured import validate_structured_disk

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def validate_structured(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The StructuredTrip json file, or a directory containing StructuredTrip json files.",
        ),
    ],
    path_out: Annotated[
        Path,
        typer.Argument(help="The output directory."),
    ],
    parsed_dir: Annotated[
        Path | None,
        typer.Option(
            help="The directory containing the ParsedTrip used to make the StructuredTrip. "
            "If not given, PATH_IN is assumed to have the ParsedTrip.",
        ),
    ] = None,
    overwrite: Annotated[
        bool,
        typer.Option(help="Allow overwriting output files."),
    ] = False,
):
    """Validate a StructuredTrip.

    The output file name will be in the form of `structured-trip_00001-01_<uuid>_errors.json
    """
    _ = ctx
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file or directory. {path_in=}")

    if path_in.is_file():
        if parsed_dir is None:
            parsed_dir = path_in.parent
        do_one(
            path_in=path_in,
            path_out=path_out,
            parsed_dir=parsed_dir,
            overwrite=overwrite,
        )
    else:
        if parsed_dir is None:
            parsed_dir = path_in
        task = progress.add_task(
            description="Validating structured trips.....", total=0
        )
        validate_structured_disk(
            path_in=path_in,
            path_out=path_out,
            parsed_dir=parsed_dir,
            overwrite=overwrite,
            task_id=task,
            progress=progress,
        )


def do_one(path_in: Path, path_out: Path, parsed_dir: Path, overwrite: bool):
    """do_one.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        parsed_dir (Path): _description_
        overwrite (bool): _description_
    """
    structured = STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=path_in)
    parsed = load_parsed(parsed_dir=parsed_dir, s_trip=structured)
    validation_model = StructuredValidation(
        parsed=parsed.resource,
        parsed_path=str(parsed.file_path),
        structured=structured,
        structured_path=str(path_in),
    )
    validator = StructuredValidator()
    validator.validate(validation_model=validation_model)
    if validation_model.errors:
        file_out = path_out / validation_model.default_file_name()
        STRUCTURED_VALIDATION_SERIALIZER.save_as_json(
            path_out=file_out, complex_obj=validation_model, overwrite=overwrite
        )
        txt_out = file_out.with_suffix(".txt")
        txt_out.write_text(str(validation_model))
        typer.echo(
            f"Found {len(validation_model.errors)} errors, debug info at {file_out}"
        )
    else:
        typer.echo(f"Found no errors")
