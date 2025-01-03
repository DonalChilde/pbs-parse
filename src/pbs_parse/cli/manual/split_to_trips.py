"""FILE: split_to_trips.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.pbs_2022_01.models.page_lines import PAGE_LINES_SERIALIZER
from pbs_parse.pbs_2022_01.models.trip_lines import TripLinesSaver
from pbs_parse.pbs_2022_01.split.extract_trips import parse_trip_lines

from ..work.progress import progress
from ..work.split_to_trips import split_to_trips_disk

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def split_to_trips(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The PageLines json file, or a directory containing PageLines json files.",
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
    """Split a page into trips.

    The output file name will be in the form of `trip-lines_00001-01_<uuid>.json
    """
    _ = ctx
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file or directory. {path_in=}")
    if path_in.is_file():
        page = PAGE_LINES_SERIALIZER.load_from_json(path_in=path_in)
        saver = TripLinesSaver(path_out=path_out)
        count = 0
        for trip in parse_trip_lines(page=page):
            count += 1
            saver(trip_lines=trip)
        typer.echo(f"Saved {count} trips to {path_out}")
    else:
        task = progress.add_task(description="Splitting pages to trips....")
        split_to_trips_disk(
            path_in=path_in,
            path_out=path_out,
            task_id=task,
            overwrite=overwrite,
            progress=progress,
        )
