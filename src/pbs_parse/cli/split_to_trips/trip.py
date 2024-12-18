"""FILE: trip.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from .common import build_job_from_file, split_to_trips_worker

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def trip(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Json file representing a page from a bid package.",
            exists=True,
            file_okay=True,
            dir_okay=False,
        ),
    ],
    path_out: Annotated[
        Path,
        typer.Argument(help="The output directory."),
    ],
    overwrite: Annotated[
        bool,
        typer.Option(help="Allow overwriting output files."),
    ] = False,
):
    """Split a page into trips."""
    _ = ctx
    job = build_job_from_file(path_in=path_in, path_out=path_out, overwrite=overwrite)
    jobs = [job]
    split_to_trips_worker(jobs=jobs)
