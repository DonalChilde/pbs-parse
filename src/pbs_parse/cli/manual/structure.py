"""FILE: structure.py."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER
from pbs_parse.pbs_2022_01.models.structured import StructuredTripSaver
from pbs_parse.pbs_2022_01.structure.parsed_to_structured import (
    structure_trip,
)

from ..work.progress import progress
from ..work.structure_trips import structure_trips_disk

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def structure(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The ParsedTrip json file, or a directory containing ParsedTrip json files.",
        ),
    ],
    path_out: Annotated[
        Path,
        typer.Argument(help="The output directory."),
    ],
    effective_from: Annotated[
        datetime,
        typer.Argument(
            help="Effective From date for bid package.", formats=["%Y-%m-%d"]
        ),
    ],
    effective_to: Annotated[
        datetime,
        typer.Argument(help="Effective to date for bid package", formats=["%Y-%m-%d"]),
    ],
    overwrite: Annotated[
        bool,
        typer.Option(help="Allow overwriting output files."),
    ] = False,
):
    """Structure a ParsedTrip.

    The output file name will be in the form of `structured-trip_00001-01_<uuid>.json
    """
    _ = ctx
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file or directory. {path_in=}")
    if path_in.is_file():
        parsed = PARSED_TRIP_SERIALIZER.load_from_json(path_in=path_in)
        saver = StructuredTripSaver(path_out=path_out)
        structured = structure_trip(
            parsed_trip=parsed,
            effective_from=effective_from.date(),
            effective_to=effective_to.date(),
        )
        out = saver(structured_trip=structured, overwrite=overwrite)
        typer.echo(f"Saved structured trip to {out}")
    else:
        with progress:
            task = progress.add_task(description="Structure trips.....")
            structure_trips_disk(
                path_in=path_in,
                path_out=path_out,
                overwrite=overwrite,
                effective_from=effective_from.date(),
                effective_to=effective_to.date(),
                task_id=task,
                progress=progress,
            )
