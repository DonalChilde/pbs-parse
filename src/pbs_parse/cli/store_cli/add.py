"""FILE: add.py."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def add(
    ctx: typer.Context,
    store_path: Annotated[
        Path,
        typer.Argument(help="Path to the data store.", exists=True, dir_okay=False),
    ],
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The pairing package PDF file.", exists=True, dir_okay=False
        ),
    ],
    base: Annotated[str, typer.Argument(help="The three letter base name, eg. PHX")],
    effective_from: Annotated[
        datetime, typer.Argument(help="Effective From date for bid package.")
    ],
    effective_to: Annotated[
        datetime, typer.Argument(help="Effective To date for bid package")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    force_clean: Annotated[
        bool, typer.Option(help="Remove exisiting before performing action.")
    ] = False,
):
    """Add a pairing package PDF file to the store."""
