"""FILE: parse_all.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

from .common import ParseActions, ParseJob, do_jobs

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def parse_all(
    ctx: typer.Context,
    store_directory: Annotated[
        Path,
        typer.Argument(
            help="Directory of the data store.", exists=True, file_okay=False
        ),
    ],
    start: Annotated[
        ParseActions,
        typer.Option(help="The action to start on. Defaults to `split_page"),
    ] = ParseActions.SPLIT_TO_PAGES,
    end: Annotated[
        ParseActions,
        typer.Option(help="The action to end at. defaults to `expand_trip`"),
    ] = ParseActions.VALIDATE_EXPANDED_TRIPS,
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    force_clean: Annotated[
        bool, typer.Option(help="Remove exisiting before performing action.")
    ] = False,
):
    """Parse the data from the text extracted from all the PDF files."""
    with StoreManager(manifest_directory=store_directory) as store:
        bases = store.get_bases()
        jobs: list[ParseJob] = []
        for base in bases:
            job = ParseJob(base=base, start=start, end=end)
            # expand_actions(job=job)
            jobs.append(job)
        do_jobs(jobs=jobs, store=store)
