"""FILE: split_to_pages.py."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer
from whenever import Date

from pbs_parse import APP_NAME
from pbs_parse.pbs_2022_01.models.bid_data import BidData, Effective
from pbs_parse.snippets.typer.task_complete import task_complete

from ..work.progress import progress
from ..work.split_to_pages import split_to_pages_disk

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def bid_to_pages(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The bid package text file.",
        ),
    ],
    path_out: Annotated[
        Path,
        typer.Argument(help="The output directory."),
    ],
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the bid month. Short, and file system friendly. e.g. 2024-01 or nov2024."
        ),
    ],
    effective_from: Annotated[
        datetime,
        typer.Argument(
            help="Effective From date for bid package.", formats=["%Y-%m-%d"]
        ),
    ],
    effective_to: Annotated[
        datetime,
        typer.Argument(help="Effective to date for bid package", formats=["%Y-%m-%d"]),
    ],
    base: Annotated[str, typer.Argument(help="The three letter base name, eg. PHX")],
    overwrite: Annotated[
        bool,
        typer.Option(help="Allow overwriting output files."),
    ] = False,
):
    """Split the text version of a PBS pairing package into pages.

    The output file name will be in the form of `page-lines_NAME_BASE_00001-00.json

    """
    _ = ctx
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file.. {path_in=}")
    bid = BidData(
        name=name,
        base=base,
        effective=Effective(
            start=Date.from_py_date(effective_from.date()),
            end=Date.from_py_date(effective_to.date()),
        ),
    )
    with progress:
        task_id = progress.add_task(description="Splitting package....", total=0)
        split_to_pages_disk(
            path_in=path_in,
            path_out=path_out,
            bid=bid,
            task_id=task_id,
            progress=progress,
            overwrite=overwrite,
        )

    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)
