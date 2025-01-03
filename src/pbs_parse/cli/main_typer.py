"""Command-line interface."""

import logging

import typer
from pfmsoft.pdf2txt.cli import extract_txt_cli

from pbs_parse.cli import (
    store_cli,
)

from .default_callback import base_options
from .manual import app as manual_app

logger = logging.getLogger(__name__)


app = typer.Typer(callback=base_options)


app.add_typer(
    store_cli.app, name="data-store", help="Use a data store for the PBS data."
)
app.add_typer(manual_app, name="manual", help="Manually execute parse commands.")
app.add_typer(extract_txt_cli.app, name="extract", help="Extract text from pdf files.")


if __name__ == "__main__":
    app()
