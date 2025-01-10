"""FILE: stats.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

import pbs_parse.pbs_2022_01.pbs_manifest as STORE
from pbs_parse import APP_NAME
from pbs_parse.snippets.typer.task_complete import task_complete

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def stats(
    ctx: typer.Context,
    store_directory: Annotated[
        Path,
        typer.Argument(
            help="Directory of the data store.", exists=True, file_okay=False
        ),
    ],
):
    """Get stats from the store."""
    store = STORE.StoreManager(manifest_directory=store_directory)
    typer.echo("Bases:")
    for base in STORE.get.bases(store=store):
        typer.echo(f"\t{base}")
    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)
