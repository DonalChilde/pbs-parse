"""FILE: parse.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def parse(
    ctx: typer.Context,
    store_path: Annotated[
        Path,
        typer.Argument(help="Path to the data store.", exists=True, dir_okay=False),
    ],
    base: Annotated[str, typer.Argument(help="The three letter base name, eg. PHX")],
    start: Annotated[
        str,
        typer.Option(help="The action to start on. Defaults to `split_page`"),
    ] = "split_page",
    end: Annotated[
        str, typer.Option(help="The action to end at. defaults to `expand_trip`")
    ] = "expand_trip",
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    force_clean: Annotated[
        bool, typer.Option(help="Remove exisiting before performing action.")
    ] = False,
):
    """Parse the data from the text extracted from a PDF file."""
