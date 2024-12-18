"""FILE: trip.py."""

import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Annotated

import typer

from .common import ParseTripJob, default_file_name, parse_worker

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def trip(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source IndexedStrings.json file.", exists=True, file_okay=True
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for parsed trip.")
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
    """Parse a `TripLines`."""
    if path_in.is_dir():
        raise typer.BadParameter("PATH_IN is a directory, should be a file.")
    if not path_in.is_file():
        raise typer.BadParameter("PATH_IN is not a file, or it doesn't exist.")
    if file_name is not None:
        dest_path = path_out / file_name
    else:
        dest_path = path_out / default_file_name(path_name=path_in.name)

    jobs: Sequence[ParseTripJob] = []
    jobs.append(
        ParseTripJob(
            split_trip_path=path_in, parsed_trip_path=dest_path, overwrite=overwrite
        )
    )
    parse_worker(jobs=jobs)
