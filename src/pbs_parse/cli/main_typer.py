"""Command-line interface."""

import datetime
import logging
from time import perf_counter_ns
from typing import Annotated

import typer
from pfmsoft.pdf2txt.cli import extract_txt_cli

from pbs_parse import APP_NAME, LOG_DIR
from pbs_parse.cli import (
    expand_trips,
    parse_trips,
    split_to_pages,
    split_to_trips,
    store_cli,
    structure_trips_cli,
)

logger = logging.getLogger(__name__)


def default_options(
    ctx: typer.Context,
    debug: Annotated[bool, typer.Option(help="Enable debug output.")] = False,
    verbosity: Annotated[int, typer.Option("-v", help="Verbosity.", count=True)] = 1,
):
    """Describe what your app does here."""
    typer.echo(f"Welcome to {APP_NAME}!")
    # typer.echo(f"{APP_NAME}'s application directory is {APP_DIR}")
    typer.echo(f"{APP_NAME}'s log directory is {LOG_DIR}")
    ctx.ensure_object(dict)
    ctx.obj["START_TIME"] = perf_counter_ns()
    ctx.obj["DEBUG"] = debug
    ctx.obj["VERBOSITY"] = verbosity
    if ctx.obj["VERBOSITY"] >= 3:
        typer.echo(f"Verbosity: {ctx.obj["VERBOSITY"]}")
        typer.echo(f"Debug: {ctx.obj["DEBUG"]}")
        dt = datetime.datetime.now(datetime.UTC)
        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S.%fZ")
        typer.echo(f"Started at: {formatted_time}")


app = typer.Typer(callback=default_options)
app_debug = typer.Typer()
app_debug.add_typer(
    extract_txt_cli.app, name="extract", help="Extract text from pdf files."
)
app_debug.add_typer(
    split_to_pages.app, name="split-pages", help="Split pages from a bid package."
)
app_debug.add_typer(
    split_to_trips.app, name="split-trips", help="Split trips from split pages."
)
app_debug.add_typer(parse_trips.app, name="parse", help="Parse split trips.")
app_debug.add_typer(
    structure_trips_cli.app, name="structure", help="Structure parsed trips."
)
app_debug.add_typer(expand_trips.app, name="expand", help="Expand structured trips.")
app.add_typer(
    store_cli.app, name="data-store", help="Use a data store for the PBS data."
)
app.add_typer(
    app_debug, name="debug", help="Manual commands for manipulating bid packages."
)

if __name__ == "__main__":
    app()
