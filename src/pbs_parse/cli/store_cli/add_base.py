"""FILE: add.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def add_base(
    ctx: typer.Context,
    store_directory: Annotated[
        Path,
        typer.Argument(
            help="Directory of the data store.", exists=True, file_okay=False
        ),
    ],
    base: Annotated[str, typer.Argument(help="The three letter base name, eg. PHX")],
    pdf_path: Annotated[
        Path,
        typer.Argument(
            help="The pairing package PDF file.", exists=True, dir_okay=False
        ),
    ],
    txt_path: Annotated[
        Path,
        typer.Argument(
            help="The pairing package TXT file.", exists=True, dir_okay=False
        ),
    ],
):
    """Add a pairing package PDF file to the store."""
    with StoreManager(manifest_directory=store_directory) as store:
        typer.echo(f"Adding {base} to store.")
        store.create_base_bid(source_pdf=pdf_path, source_txt=txt_path, name=base)
