"""FILE: expand.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse import APP_NAME
from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.snippets.typer.task_complete import task_complete

from ..work.expand_trips import expand_trips_disk
from ..work.progress import progress

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def expand(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The ParsedTrip json file, or a directory containing ParsedTrip json files.",
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
    debug_dir: Annotated[
        Path | None, typer.Option(help="The directory for debug output.")
    ] = None,
):
    """Expand a ParsedTrip.

    The output file name will be in the form of `expanded-trip_00001-01_<uuid>.json`
    """
    _ = ctx
    if debug_dir is not None and debug_dir.is_file():
        typer.BadParameter(
            f"DEBUG_DIR must be a directory or None, not a file. {debug_dir=}"
        )
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file or directory. {path_in=}")
    if path_in.is_file():
        parsed_paths = [path_in]
    else:
        parsed_paths = API.find.parsed_trips(dir_in=path_in)
    with progress:
        task = progress.add_task(description="Expand trips.....")
        expand_trips_disk(
            parsed_paths=parsed_paths,
            path_out=path_out,
            overwrite=overwrite,
            task_id=task,
            progress=progress,
            debug_dir=debug_dir,
        )
    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)
