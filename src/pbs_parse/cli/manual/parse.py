"""FILE: parse.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse import APP_NAME
from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.snippets.typer.task_complete import task_complete

from ..work.parse_trips import parse_trips_disk
from ..work.progress import progress

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def parse_trips(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The TripLines json file, or a directory containing TripLines json files.",
        ),
    ],
    path_out: Annotated[
        Path,
        typer.Argument(help="The output directory."),
    ],
    overwrite: Annotated[
        bool,
        typer.Option(help="Allow overwriting output files."),
    ] = False,
):
    """Parse a TripLines.

    The output file name will be in the form of `parsed-trip_00001-01_<uuid>.json
    """
    _ = ctx
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file or directory. {path_in=}")
    if path_in.is_file():
        trip_paths = [path_in]
    else:
        trip_paths = API.find.trip_lines(dir_in=path_in)
    with progress:
        task = progress.add_task(description="Parsing trips.....", total=0)
        parse_trips_disk(
            trip_paths=trip_paths,
            path_out=path_out,
            overwrite=overwrite,
            task_id=task,
            progress=progress,
        )
    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)
