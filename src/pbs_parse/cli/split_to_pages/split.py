"""FILE: split.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from .common import build_job_from_file, build_jobs_from_dir, split_to_pages_worker

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def split(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The bid package text file, or a directory containing bid package text files.",
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
    """Split the text version of a PBS pairing package into pages.

    The output file name will be in the form of `page-lines_00001-00_<uuid>.json
    If splitting multiple files, files will be output to PATH_OUT/PATH_IN/file.stem/pages/
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
    split_to_pages_worker(jobs=jobs)
