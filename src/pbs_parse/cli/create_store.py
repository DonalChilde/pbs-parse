"""FILE: create_store.py."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.pbs_2022_01.pbs_store.store_manager import StoreManager

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def create_store(
    ctx: typer.Context,
    store_dir: Annotated[
        Path,
        typer.Argument(help="Directory of the data store."),
    ],
    name: Annotated[
        str, typer.Argument(help="The name for the bid period, eg Nov2024.")
    ],
    effective_from: Annotated[
        datetime,
        typer.Argument(
            help="Effective From date for bid package.", formats=["%Y-%m-%d"]
        ),
    ],
    effective_to: Annotated[
        datetime,
        typer.Argument(help="Effective To date for bid package", formats=["%Y-%m-%d"]),
    ],
):
    """Create a PBS data store in the STORE_DIR directory."""
    if store_dir.is_file():
        raise typer.BadParameter(f"Store directory is an existing file. {store_dir=}")
    StoreManager.init_manifest(
        manifest_directory=store_dir,
        name=name,
        effective_from=effective_from.date(),
        effective_to=effective_to.date(),
    )
    typer.echo(f"Created a new pbs data store at {store_dir}")
