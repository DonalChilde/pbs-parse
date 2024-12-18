"""FILE: all_trips.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from .common import build_jobs_from_directory, rich_worker

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def all_trips(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Directory of trip lines files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="Destination directory for parsed trips.")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
):
    """Parse all the `TripLines`."""
    jobs = build_jobs_from_directory(
        path_in=path_in, path_out=path_out, overwrite=overwrite
    )
    rich_worker(jobs=jobs)
