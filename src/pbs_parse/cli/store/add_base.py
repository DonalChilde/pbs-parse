"""FILE: add_base.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

import pbs_parse.pbs_2022_01.pbs_store as STORE
from pbs_parse import APP_NAME
from pbs_parse.snippets.typer.task_complete import task_complete

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
    store = STORE.StoreManager(manifest_directory=store_directory)
    with store:
        store_name = STORE.get.name(store=store)
        store.create_base_bid(source_pdf=pdf_path, source_txt=txt_path, name=base)
        typer.echo(f"Added {base} to {store_name} store.")
    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)
