"""FILE: rebuild.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def rebuild(
    ctx: typer.Context,
    store_path: Annotated[
        Path,
        typer.Argument(help="Path to the data store.", exists=True, dir_okay=False),
    ],
    force_clean: Annotated[
        bool, typer.Option(help="Remove exisiting before performing action.")
    ] = False,
):
    """Rebuild the store data from actual files."""
