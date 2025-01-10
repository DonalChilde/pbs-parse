"""FILE: split_to_pages.py."""

import logging
from pathlib import Path
from typing import Annotated, TypedDict

import typer
from rich.progress import TaskID

from pbs_parse import APP_NAME
from pbs_parse.snippets.typer.task_complete import task_complete

from ..work.progress import progress
from ..work.split_to_pages import split_to_pages_disk

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def split_to_pages(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The bid package text file, or a directory containing bid package text files.",
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
    """Split the text version of a PBS pairing package into pages.

    The output file name will be in the form of `page-lines_00001-00_<uuid>.json
    If splitting multiple files, files will be output to PATH_OUT/<PATH_IN/file.stem>/pages/
    """
    _ = ctx
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file or directory. {path_in=}")
    if path_in.is_file():
        do_one(path_in=path_in, path_out=path_out, overwrite=overwrite)
    else:
        do_many(path_in=path_in, path_out=path_out, overwrite=overwrite)
    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)


def do_one(path_in: Path, path_out: Path, overwrite: bool):
    """do_one.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
    """
    with progress:
        task_id = progress.add_task(description="Splitting package....", total=0)
        split_to_pages_disk(
            path_in=path_in,
            path_out=path_out,
            task_id=task_id,
            progress=progress,
            overwrite=overwrite,
        )


class Job(TypedDict):
    """Job."""

    path_in: Path
    path_out: Path
    task_id: TaskID


def do_many(path_in: Path, path_out: Path, overwrite: bool):
    """do_many.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        overwrite (bool): _description_
    """
    txt_files = list(path_in.glob("*.txt", case_sensitive=False))
    jobs: list[Job] = []
    task_job = progress.add_task(
        description="Splitting packages to pages....", total=len(txt_files)
    )
    for txt_file in txt_files:
        jobs.append(
            Job(
                path_in=txt_file,
                path_out=path_out / path_in.stem,
                task_id=progress.add_task(
                    description="Splitting package....WAITING", total=0
                ),
            )
        )
    with progress:
        for job in jobs:
            split_to_pages_disk(**job, overwrite=overwrite, progress=progress)
            progress.advance(task_id=task_job, advance=1)
