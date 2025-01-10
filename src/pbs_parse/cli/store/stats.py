"""FILE: stats.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse import APP_NAME
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager
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
    store = StoreManager(manifest_directory=store_directory)
    typer.echo("Bases:")
    for base in store.get_bases():
        typer.echo(f"\t{base}")
    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)
