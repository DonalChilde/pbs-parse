"""FILE: all_trips.py."""

from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from .common import build_jobs_from_directory, rich_worker

app = typer.Typer()

import logging

logger = logging.getLogger(__name__)


@app.command()
def all_trips(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="directory containing `ParsedTrip` .json files.",
            exists=True,
            file_okay=False,
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for structured trips files.")
    ],
    effective_from: Annotated[
        datetime, typer.Argument(help="Effective From date for bid package.")
    ],
    effective_to: Annotated[
        datetime, typer.Argument(help="Effective To date for bid package")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
):
    """Structure all the parsed trips in a directory."""
    jobs = build_jobs_from_directory(
        path_in=path_in,
        path_out=path_out,
        effective_from=effective_from.date(),
        effective_to=effective_to.date(),
        overwrite=overwrite,
    )
    rich_worker(jobs=jobs)
