"""FILE: page.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from .common import build_job_from_file, rich_worker

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def page(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The bid package text file.",
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
    """Split the text version of a PBS pairing package into pages."""
    _ = ctx
    job = build_job_from_file(path_in=path_in, path_out=path_out, overwrite=overwrite)
    jobs = [job]
    rich_worker(jobs=jobs)
