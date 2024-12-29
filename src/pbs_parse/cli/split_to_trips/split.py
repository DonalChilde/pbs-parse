"""FILE: split.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from .common import build_job_from_file, build_jobs_from_dir, split_to_trips_worker

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def split(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Json file representing a page from a bid package, or a directory containing json files.",
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
    """Split a page into trips.

    The output file name will be in the form of `trip-lines_00001-01_<uuid>.json
    """
    _ = ctx
    if path_in.is_file():
        job = build_job_from_file(
            path_in=path_in, path_out=path_out, overwrite=overwrite
        )
        jobs = [job]
    elif path_in.is_dir():
        jobs = build_jobs_from_dir(
            path_in=path_in, path_out=path_out, overwrite=overwrite
        )
    else:
        raise typer.BadParameter("path in must be a file or directory.")
    split_to_trips_worker(jobs=jobs)
