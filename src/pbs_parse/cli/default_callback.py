"""The main callback function."""

import logging
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter_ns
from typing import Annotated, TypedDict

import typer

from pbs_parse import APP_DIR, APP_NAME, LOG_DIR

logger = logging.getLogger(__name__)


class AppData(TypedDict):
    """App data to be stored on ctx."""

    app_name: str
    log_dir: Path
    app_dir: Path
    start_perf: int
    start_time: datetime
    debug: bool
    verbosity: int
    connection_string: str
    connection_type: str


def base_options(
    ctx: typer.Context,
    debug: Annotated[bool, typer.Option(help="Enable debug output.")] = False,
    verbosity: Annotated[int, typer.Option("-v", help="Verbosity.", count=True)] = 1,
):
    """Describe what your app does here."""
    app_data = AppData(
        app_name=APP_NAME,
        log_dir=LOG_DIR,
        app_dir=APP_DIR,
        start_perf=perf_counter_ns(),
        start_time=datetime.now(UTC),
        debug=debug,
        verbosity=verbosity,
        connection_string="",
        connection_type="",
    )
    typer.echo(f"Welcome to {APP_NAME}!")
    # typer.echo(f"{APP_NAME}'s application directory is {APP_DIR}")
    typer.echo(f"{APP_NAME}'s log directory is {LOG_DIR}")
    ctx.ensure_object(dict)
    ctx.obj[APP_NAME] = app_data
    if ctx.obj[APP_NAME]["verbosity"] >= 3:
        typer.echo(f"Verbosity: {ctx.obj[APP_NAME]["verbosity"]}")
        typer.echo(f"Debug: {ctx.obj[APP_NAME]["debug"]}")
        formatted_time = ctx.obj[APP_NAME]["start_time"].strftime(
            "%Y-%m-%d %H:%M:%S.%fZ"
        )
        typer.echo(f"Started at: {formatted_time}")
