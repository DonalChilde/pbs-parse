"""FILE: trip.py."""

from pathlib import Path
from typing import Annotated

import typer

from .common import ExpandTripJob, expand_worker

app = typer.Typer()

import logging

logger = logging.getLogger(__name__)


@app.command()
def trip(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source structured trip .json file.", exists=True, file_okay=True
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for expanded trips.")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
):
    """Expand the structured trip."""
    if path_in.is_dir():
        raise typer.BadParameter("PATH_IN is a directory, should be a file.")
    if path_out.is_file():
        raise typer.BadParameter("PATH_OUT is a file and should be a directory.")
    if not path_in.is_file():
        raise typer.BadParameter("PATH_IN is not a file, or it doesn't exist.")

    jobs: list[ExpandTripJob] = []
    jobs.append(
        ExpandTripJob(
            s_trip_path=path_in,
            dir_path_out=path_out,
            overwrite=overwrite,
        )
    )
    expand_worker(jobs=jobs)
