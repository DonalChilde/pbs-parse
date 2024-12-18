"""FILE: all_pages.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from .common import build_jobs_from_dir, rich_worker

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def all_pages(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="A directory containing the bid package text files.",
            exists=True,
            dir_okay=True,
            file_okay=False,
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
    """Split multiple text PBS pairing packages into pages.

    Files will be output to PATH_OUT/PATH_IN.stem/pages/
    """
    _ = ctx
    jobs = build_jobs_from_dir(path_in=path_in, path_out=path_out, overwrite=overwrite)
    rich_worker(jobs=jobs)
