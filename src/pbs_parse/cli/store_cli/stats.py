"""FILE: stats.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def stats(
    ctx: typer.Context,
    store_path: Annotated[
        Path,
        typer.Argument(help="Path to the data store.", exists=True, dir_okay=False),
    ],
):
    """Get stats from the store."""
