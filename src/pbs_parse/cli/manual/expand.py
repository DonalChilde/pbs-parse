"""FILE: expand.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.pbs_2022_01.expand.structured_to_expanded import StructuredToExpanded
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTripSaver
from pbs_parse.pbs_2022_01.models.structured import STRUCTURED_TRIP_SERIALIZER

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
            help="The StructuredTrip json file, or a directory containing StructuredTrip json files.",
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
    """Expand a StructuredTrip.

    The output file name will be in the form of `expanded-trip_00001-01_<uuid>.json`
    """
    _ = ctx
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file or directory. {path_in=}")
    if path_in.is_file():
        structured = STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=path_in)
        saver = ExpandedTripSaver(path_out=path_out)
        expander = StructuredToExpanded(structured_trip=structured)
        idx = 0
        out = Path("")
        for idx, trip in enumerate(expander.translate(), start=1):
            _ = idx
            out = saver(expanded_trip=trip, overwrite=overwrite)
        typer.echo(f"Saved {idx} expanded trips to {out.parent}")
    else:
        task = progress.add_task(description="Expand trips.....")
        expand_trips_disk(
            path_in=path_in,
            path_out=path_out,
            overwrite=overwrite,
            task_id=task,
            progress=progress,
        )
