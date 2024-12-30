"""FILE: parse.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

from .common import ParseActions, ParseJob, do_jobs

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def parse(
    ctx: typer.Context,
    store_directory: Annotated[
        Path,
        typer.Argument(
            help="Directory of the data store.", exists=True, file_okay=False
        ),
    ],
    base: Annotated[str, typer.Argument(help="The three letter base name, eg. PHX")],
    start: Annotated[
        ParseActions,
        typer.Option(help="The action to start on."),
    ] = ParseActions.SPLIT_TO_PAGES,
    end: Annotated[
        ParseActions,
        typer.Option(help="The action to end at."),
    ] = ParseActions.EXPAND_TRIPS,
):
    """Parse the data from the text extracted from a PDF file."""
    _ = ctx
    with StoreManager(manifest_directory=store_directory) as store:
        jobs: list[ParseJob] = []
        job = ParseJob(base=base, start=start, end=end)
        jobs.append(job)
        do_jobs(jobs=jobs, store=store)
