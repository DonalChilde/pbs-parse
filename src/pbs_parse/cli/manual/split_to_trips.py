"""FILE: split_to_trips.py."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse import APP_NAME
from pbs_parse.pbs_2022_01.models.page_lines import (
    PAGE_LINES_SERIALIZER,
    PageLines,
    PageLinesLoader,
)
from pbs_parse.snippets.file.data_file_loader import FileResource
from pbs_parse.snippets.typer.task_complete import task_complete

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
        page_resource = FileResource[PageLines](
            resource=PAGE_LINES_SERIALIZER.load_from_json(path_in=path_in),
            file_path=path_in,
        )
        page_resources = [page_resource]
        page_count = 1

    else:
        page_loader = PageLinesLoader(path_in=path_in)
        page_resources = iter(page_loader)
        page_count = len(page_loader)

    with progress:
        task = progress.add_task(description="Splitting pages to trips....")
        split_to_trips_disk(
            page_resources=page_resources,
            page_count=page_count,
            path_out=path_out,
            task_id=task,
            overwrite=overwrite,
            progress=progress,
        )
    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)
