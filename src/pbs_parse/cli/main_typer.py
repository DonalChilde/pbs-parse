"""Command-line interface."""

import logging

import typer
from pfmsoft.pdf2txt.cli import extract_txt_cli

from pbs_parse.cli import (
    expand_trips,
    parse_trips,
    split_to_pages,
    split_to_trips,
    store_cli,
    structure_trips,
)

from .default_callback import base_options

logger = logging.getLogger(__name__)


app = typer.Typer(callback=base_options)
app_debug = typer.Typer()

app_debug.add_typer(
    split_to_pages.app,
    name="packages",
    short_help="Split pages from a bid package.",
)
app_debug.add_typer(
    split_to_trips.app, name="pages", help="Split trips from split pages."
)
app_debug.add_typer(parse_trips.app, name="parse", help="Parse split trips.")
app_debug.add_typer(
    structure_trips.app, name="structure", help="Structure parsed trips."
)
app_debug.add_typer(expand_trips.app, name="expand", help="Expand structured trips.")

app.add_typer(
    store_cli.app, name="data-store", help="Use a data store for the PBS data."
)
app.add_typer(extract_txt_cli.app, name="extract", help="Extract text from pdf files.")
app.add_typer(
    app_debug, name="debug", help="Manual commands for manipulating bid packages."
)

if __name__ == "__main__":
    app()
