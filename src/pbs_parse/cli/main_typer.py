"""Command-line interface."""

import datetime
import logging
from pathlib import Path
from time import perf_counter_ns
from typing import Annotated

import typer

from pbs_parse.cli import (
    parse_trips_cli,
    split_pages_cli,
    split_trips_cli,
    structure_trips_cli,
)

logger = logging.getLogger(__name__)

APP_NAME = "pbs-parse"


def app_dir() -> Path:
    """Get the system approiate application directory.

    Returns:
        _type_: The app dir.
    """
    return Path(typer.get_app_dir(app_name=APP_NAME))


def default_options(
    ctx: typer.Context,
    debug: Annotated[bool, typer.Option(help="Enable debug output.")] = False,
    verbosity: Annotated[int, typer.Option("-v", help="Verbosity.", count=True)] = 1,
):
    """Describe what your app does here."""
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
app.add_typer(parse_trips_cli.app, name="parse", help="Parse split trips.")
app.add_typer(structure_trips_cli.app, name="structure", help="Structure parsed trips.")
app.add_typer(
    split_pages_cli.app, name="split-pages", help="Split pages from a bid package."
)
app.add_typer(split_trips_cli.app, name="split-trips", help="Split trips from pages.")

if __name__ == "__main__":
    app()
