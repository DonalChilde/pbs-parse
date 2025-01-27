"""FILE: expanded_debug.py."""

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
def expanded_debug(
    ctx: typer.Context,
    store_directory: Annotated[
        Path,
        typer.Argument(
            help="Directory of the data store.", exists=True, file_okay=False
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
    """Export Expanded trip debug data."""
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    store = STORE.StoreManager(manifest_directory=store_directory)
    store_name = STORE.get.name(store=store)
    typer.echo(f"Checking for expanded trip errors in {store_name}")
    bases = STORE.get.bases(store=store)
    error_count = 0
    bases_with_errors: list[str] = []
    for base in bases:
        expanded_keys = STORE.get.expanded_errors_keys(store=store, base=base)
        if expanded_keys:
            error_count += len(expanded_keys)
            bases_with_errors.append(base)
    typer.echo(f"Found {error_count} trips with errors.")
    for base in bases_with_errors:
        dir_out = path_out / store_name / base / "expanded"
        STORE.export.expanded_debug(
            store=store, base=base, dir_out=dir_out, overwrite=overwrite
        )
    if bases_with_errors:
        typer.echo(f"Debug info written to {path_out}/STORE_NAME/BASE/expanded")

    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)
