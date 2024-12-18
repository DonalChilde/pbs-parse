"""FILE: all_trips.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from .common import build_jobs_from_dir, split_to_trips_worker

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def all_trips(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="A directory containing json files representing trips from a bid package.",
            exists=True,
            file_okay=False,
            dir_okay=True,
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
    """Split all the pages found in a directory into trips."""
    _ = ctx
    jobs = build_jobs_from_dir(path_in=path_in, path_out=path_out, overwrite=overwrite)
    split_to_trips_worker(jobs=jobs)
