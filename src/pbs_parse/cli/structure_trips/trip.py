"""FILE: trip.py."""

from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from .common import StructureTripJob, default_file_name, rich_worker

app = typer.Typer()

import logging

logger = logging.getLogger(__name__)


@app.command()
def trip(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source `ParsedTrip` .json file.", exists=True, file_okay=True
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for structured trip.")
    ],
    effective_from: Annotated[
        datetime, typer.Argument(help="Effective From date for bid package.")
    ],
    effective_to: Annotated[
        datetime, typer.Argument(help="Effective To date for bid package")
    ],
    file_name: Annotated[
        Path | None,
        typer.Option(help="file name for output if differrent from default."),
    ] = None,
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
):
    """Structure a `ParsedTrip`."""
    if path_in.is_dir():
        raise typer.BadParameter("PATH_IN is a directory, should be a file.")
    if not path_in.is_file():
        raise typer.BadParameter("PATH_IN is not a file, or it doesn't exist.")
    if file_name is not None:
        dest_path = path_out / file_name
    else:
        dest_path = path_out / f"{default_file_name(path_in=path_in)}"

    jobs: list[StructureTripJob] = []
    jobs.append(
        StructureTripJob(
            parsed_trip_path=path_in,
            structured_trip_path=dest_path,
            overwrite=overwrite,
            effective_from=effective_from.date(),
            effective_to=effective_to.date(),
        )
    )
    rich_worker(jobs=jobs)
