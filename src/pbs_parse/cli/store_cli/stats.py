"""FILE: stats.py."""

import logging

import typer

from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def stats(
    ctx: typer.Context,
):
    """Get stats from the store."""
    store: StoreManager = ctx.obj["DISK_STORE"]
    typer.echo("Bases:")
    for base in store.get_bases():
        typer.echo(f"\t{base}")
