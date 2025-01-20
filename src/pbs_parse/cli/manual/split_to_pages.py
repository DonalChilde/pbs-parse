"""FILE: split_to_pages.py."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated, TypedDict

import typer
from rich.progress import TaskID

from pbs_parse import APP_NAME
from pbs_parse.pbs_2022_01.models.external_data import ExternalData
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
    base: Annotated[
        str, typer.Option(help="The three letter base name, eg. PHX")
    ] = "auto-detect",
    overwrite: Annotated[
        bool,
        typer.Option(help="Allow overwriting output files."),
    ] = False,
):
    """Split the text version of a PBS pairing package into pages.

    If the base is `auto-detect` then the base name will be parsed from the file name,
    assuming the file name matches the pattern `PBS_CLT_December_2024_20241108121007.pdf`.

    The output directory will be PATH_OUT/BASE/pages
    The output file name will be in the form of `page-lines_EFFECTIVE_FROM_EFFECTIVE_TO_BASE_00001-00.json

    """
    _ = ctx
    if path_out.is_file():
        typer.BadParameter(f"Path out must be a directory, not a file. {path_out=}")
    if not path_in.exists():
        typer.BadParameter(f"Path in must be an existing file or directory. {path_in=}")
    external = ExternalData(
        effective_from=effective_from.date(), effective_to=effective_to.date()
    )
    if path_in.is_file():
        if base == "auto-detect":
            external.base = parse_base_name(path_in.stem)
        else:
            external.base = base
        do_one(
            path_in=path_in, path_out=path_out, external=external, overwrite=overwrite
        )
    else:
        do_many(
            path_in=path_in, path_out=path_out, external=external, overwrite=overwrite
        )
    start_perf = ctx.obj[APP_NAME]["start_perf"]
    task_complete(start_perf=start_perf)


def parse_base_name(file_name: str) -> str:
    """Get the base name from a file name.

    Expects a file name in the form of `PBS_CLT_December_2024_20241108121007.pdf`
    """
    tokens = file_name.split("_")
    return tokens[1]


class Job(TypedDict):
    """Job."""

    path_in: Path
    path_out: Path
    external: ExternalData
    task_id: TaskID


def do_one(path_in: Path, path_out: Path, external: ExternalData, overwrite: bool):
    """do_one.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        external (ExternalData): _description_
        overwrite (bool): _description_
    """
    with progress:
        task_id = progress.add_task(description="Splitting package....", total=0)
        job = Job(
            path_in=path_in,
            path_out=path_out / external.base / "pages",
            external=external,
            task_id=task_id,
        )
        split_to_pages_disk(**job, progress=progress, overwrite=overwrite)


def do_many(path_in: Path, path_out: Path, external: ExternalData, overwrite: bool):
    """do_many.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        external (ExternalData): _description_
        overwrite (bool): _description_
    """
    txt_files = list(path_in.glob("PBS_*.txt", case_sensitive=False))
    jobs: list[Job] = []
    task_job = progress.add_task(
        description="Splitting packages to pages....", total=len(txt_files)
    )
    for txt_file in txt_files:
        _external = ExternalData(
            base=parse_base_name(txt_file.stem),
            effective_from=external.effective_from,
            effective_to=external.effective_to,
        )
        jobs.append(
            Job(
                path_in=txt_file,
                path_out=path_out / _external.base / "pages",
                external=_external,
                task_id=progress.add_task(
                    description="Splitting package....WAITING", total=0
                ),
            )
        )
    with progress:
        for job in jobs:
            split_to_pages_disk(**job, overwrite=overwrite, progress=progress)
            progress.advance(task_id=task_job, advance=1)
