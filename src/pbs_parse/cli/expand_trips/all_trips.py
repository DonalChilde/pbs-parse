"""FILE: all_trips.py."""

from pathlib import Path
from typing import Annotated

import typer

from .common import build_jobs_from_directory, expand_worker

app = typer.Typer()

import logging

logger = logging.getLogger(__name__)


@app.command()
def all_trips(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="directory containing structured trip .json files.",
            exists=True,
            file_okay=False,
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for expanded trip files.")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
):
    """Expand all the structured trips found in PATH_IN."""
    jobs = build_jobs_from_directory(
        path_in=path_in,
        path_out=path_out,
        overwrite=overwrite,
    )
    expand_worker(jobs=jobs)
