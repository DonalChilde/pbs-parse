"""FILE: structure.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse import APP_NAME
from pbs_parse.pbs_2022_01.models.parsed_trip import (
    PARSED_TRIP_SERIALIZER,
    ParsedTripLoader,
)
from pbs_parse.snippets.file.data_file_loader import FileResource
from pbs_parse.snippets.typer.task_complete import task_complete

from ..work.progress import progress
from ..work.structure_trips import structure_trips_disk

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def structure(
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
):
    """Structure a ParsedTrip.

    The output file name will be in the form of `structured-trip_00001-01_<uuid>.json
    """
    _ = ctx
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file or directory. {path_in=}")
    if path_in.is_file():
        parsed_resource = FileResource(
            resource=PARSED_TRIP_SERIALIZER.load_from_json(path_in=path_in),
            file_path=path_in,
        )
        parsed_resources = [parsed_resource]
        parsed_count = 1
    else:
        loader = ParsedTripLoader(path_in=path_in)
        parsed_resources = iter(loader)
        parsed_count = len(loader)
    with progress:
        task = progress.add_task(description="Structure trips.....")
        structure_trips_disk(
            parsed_resources=parsed_resources,
            parsed_count=parsed_count,
            path_out=path_out,
            overwrite=overwrite,
            task_id=task,
            progress=progress,
        )
    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)
