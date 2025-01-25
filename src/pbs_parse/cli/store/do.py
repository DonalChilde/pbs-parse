"""FILE: do.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse import APP_NAME
from pbs_parse.snippets.typer.task_complete import task_complete

from .common import ParseActions, ParseJob, do_jobs

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def do(
    ctx: typer.Context,
    store_directory: Annotated[
        Path,
        typer.Argument(
            help="Directory of the data store.", exists=True, file_okay=False
        ),
    ],
    bases: Annotated[
        list[str],
        typer.Argument(
            help="A list of bases to perform actions on. `_all_` will do the actions on all bases."
        ),
    ],
    start: Annotated[
        ParseActions,
        typer.Option(help="The action to start on. Defaults to `split_page"),
    ] = ParseActions.SPLIT_TO_PAGES,
    end: Annotated[
        ParseActions,
        typer.Option(help="The action to end at. defaults to `expand_trip`"),
    ] = ParseActions.EXPAND_TRIPS,
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
):
    """Parse the data from the text extracted from all the PDF files."""
    store = STORE.StoreManager(manifest_directory=store_directory)
    with store:
        bases_in_store = STORE.get.bases(store=store)
        if "_all_" in bases:
            bases = bases_in_store
        else:
            for base in bases:
                if base not in bases_in_store:
                    raise typer.BadParameter(
                        f"{base=} is not in the store. {bases_in_store=}"
                    )
        jobs: list[ParseJob] = []
        for base in bases:
            job = ParseJob(base=base, start=start, end=end, overwrite=overwrite)
            jobs.append(job)
        do_jobs(jobs=jobs, store=store)
    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)
