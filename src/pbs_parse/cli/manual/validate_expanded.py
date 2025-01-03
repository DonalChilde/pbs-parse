"""FILE: validate_expanded.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.cli.work.common import load_parsed, load_structured
from pbs_parse.pbs_2022_01.models.expanded import EXPANDED_TRIP_SERIALIZER
from pbs_parse.pbs_2022_01.models.expanded_validation import (
    EXPANDED_VALIDATION_SERIALIZER,
    ExpandedValidation,
)
from pbs_parse.pbs_2022_01.validate.validate_expanded import ExpandedValidator

from ..work.progress import progress
from ..work.validate_expanded import validate_expanded_disk

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def validate_expanded(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The ExpandedTrip json file, or a directory containing ExpandedTrip json files.",
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
    structured_dir: Annotated[
        Path | None,
        typer.Option(
            help="The directory containing the StructuredTrip used to make the ExpandedTrip. "
            "If not given, PATH_IN is assumed to have the StructuredTrip.",
        ),
    ] = None,
    overwrite: Annotated[
        bool,
        typer.Option(help="Allow overwriting output files."),
    ] = False,
):
    """Validate an ExpandedTrip.

    The output file name will be in the form of `expanded-trip_00001-01_<uuid>_errors.json
    """
    _ = ctx
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file or directory. {path_in=}")

    if path_in.is_file():
        if parsed_dir is None:
            parsed_dir = path_in.parent
        if structured_dir is None:
            structured_dir = path_in.parent
        do_one(
            path_in=path_in,
            path_out=path_out,
            parsed_dir=parsed_dir,
            structured_dir=structured_dir,
            overwrite=overwrite,
        )
    else:
        if parsed_dir is None:
            parsed_dir = path_in
        if structured_dir is None:
            structured_dir = path_in
        task = progress.add_task(description="Validating expanded trips.....", total=0)
        validate_expanded_disk(
            path_in=path_in,
            path_out=path_out,
            parsed_dir=parsed_dir,
            structured_dir=structured_dir,
            overwrite=overwrite,
            task_id=task,
            progress=progress,
        )


def do_one(
    path_in: Path,
    path_out: Path,
    parsed_dir: Path,
    structured_dir: Path,
    overwrite: bool,
):
    """do_one.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        parsed_dir (Path): _description_
        structured_dir (Path): _description_
        overwrite (bool): _description_
    """
    expanded = EXPANDED_TRIP_SERIALIZER.load_from_json(path_in=path_in)
    structured = load_structured(structured_dir=structured_dir, e_trip=expanded)
    validation_model = ExpandedValidation(
        expanded=expanded,
        parsed_path=str(path_in),
        structured=structured.resource,
        structured_path=str(structured.file_path),
    )
    validator = ExpandedValidator()
    validator.validate(validation_model=validation_model)
    if validation_model.errors:
        file_out = path_out / validation_model.default_file_name()
        parsed = load_parsed(parsed_dir=parsed_dir, s_trip=structured.resource)
        validation_model.parsed = parsed.resource
        validation_model.parsed_path = str(parsed.file_path)
        EXPANDED_VALIDATION_SERIALIZER.save_as_json(
            path_out=file_out, complex_obj=validation_model, overwrite=overwrite
        )
        txt_out = file_out.with_suffix(".txt")
        txt_out.write_text(str(validation_model))
        typer.echo(
            f"Found {len(validation_model.errors)} errors, debug info at {file_out}"
        )
    else:
        typer.echo(f"Found no errors")
