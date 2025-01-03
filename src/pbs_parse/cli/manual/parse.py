"""FILE: parse.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer
from pfmsoft.state_parser import ParseContext

from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTripSaver
from pbs_parse.pbs_2022_01.models.trip_lines import TRIP_LINES_SERIALIZER
from pbs_parse.pbs_2022_01.parse.trip_lines_parser import TripLinesParser

from ..work.parse_trips import parse_trips_disk
from ..work.progress import progress

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def parse(
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
        trip_lines = TRIP_LINES_SERIALIZER.load_from_json(path_in=path_in)
        parse_ctx = ParseContext()
        parser = TripLinesParser()
        parsed = parser.parse(ctx=parse_ctx, trip_lines=trip_lines)
        out = ParsedTripSaver(path_out=path_out)(parsed_trip=parsed)
        typer.echo(f"Saved parsed trip to {out}")
    else:
        task = progress.add_task(description="Parsing trips.....", total=0)
        parse_trips_disk(
            path_in=path_in,
            path_out=path_out,
            overwrite=overwrite,
            task_id=task,
            progress=progress,
        )
