"""Typer cli to split pbs package txt to pages."""

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from rich.progress import (
    BarColumn,
    FileSizeColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TotalFileSizeColumn,
)

from pbs_parse.pbs_2022_01.split.extract_pages import (
    parse_page_lines_from_file,
    write_page_lines,
)

logger = logging.getLogger(__name__)
app = typer.Typer()


@dataclass
class SplitPageJob:
    """Job container."""

    path_in: Path
    path_out: Path
    overwrite: bool = False


def total_size_of_files(jobs: Sequence[SplitPageJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.path_in.stat().st_size
    return total


@app.command()
def page(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The bid package text file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
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
    """Split the text version of a PBS pairing package into pages."""
    _ = ctx
    job = build_job_from_file(path_in=path_in, path_out=path_out, overwrite=overwrite)
    jobs = [job]
    extract_pages_rich(jobs=jobs)


@app.command()
def all(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="A directory containing the bid package text files.",
            exists=True,
            dir_okay=True,
            file_okay=False,
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
    """Split multiple text PBS pairing packages into pages.

    Files will be output to PATH_OUT/PATH_IN.stem/pages/
    """
    _ = ctx
    jobs = build_jobs_from_dir(path_in=path_in, path_out=path_out, overwrite=overwrite)
    extract_pages_rich(jobs=jobs)


def build_job_from_file(path_in: Path, path_out: Path, overwrite: bool) -> SplitPageJob:
    """Check for valid inputs and return a `SplitPageJob`."""
    if path_in.is_file():
        if path_in.suffix.lower() != ".txt":
            raise typer.BadParameter(
                f"Input path might not be a valid file, it does not have a .txt suffix. {path_in}"
            )
    else:
        raise typer.BadParameter(f"Input path is not a valid file. {path_in}")
    if path_out.is_file():
        raise typer.BadParameter(
            f"Output path is a file, it should be a directory. {path_out}"
        )
    job = SplitPageJob(path_in=path_in, path_out=path_out, overwrite=overwrite)
    return job


def build_jobs_from_dir(
    path_in: Path, path_out: Path, overwrite: bool
) -> Sequence[SplitPageJob]:
    """Collect text files, and use to build `SplitPageJob`s."""
    glob = "*.txt"
    if not path_in.is_dir():
        raise typer.BadParameter("PATH_IN should be a directory.")
    typer.echo("Collecting bid packages to split into pages.....")
    typer.echo(f"Looking for files in {path_in}")
    files = [f for f in path_in.glob(glob, case_sensitive=False) if f.is_file()]
    typer.echo(f"Found {len(files)} text files.")
    if len(files) == 0:
        raise typer.BadParameter(
            "Input path is not a directory containing valid files.\n"
            f"Files are expected to match {glob}"
        )
    jobs: list[SplitPageJob] = []
    for file in files:
        out_path = path_out / file.stem / "pages"
        job = build_job_from_file(path_in=file, path_out=out_path, overwrite=overwrite)
        jobs.append(job)
    return jobs


# def collect_jobs(
#     path_in: Path, path_out: Path, overwrite: bool
# ) -> Sequence[SplitPageJob]:
#     """Build a collections of jobs to do."""
#     if path_in.is_dir():
#         files = [f for f in path_in.glob(".txt", case_sensitive=False) if f.is_file()]
#     elif path_in.is_file():
#         files = [path_in]
#     else:
#         raise typer.BadParameter(
#             "Input path is not a valid file, or directory containing valid files."
#         )
#     jobs: list[SplitPageJob] = []
#     for file in files:
#         if len(files) > 1:
#             dest_dir = path_out / Path(file.stem) / Path("pages")
#         else:
#             dest_dir = path_out
#         jobs.append(SplitPageJob(path_in=file, path_out=dest_dir, overwrite=overwrite))
#     return jobs


def extract_pages_rich(jobs: Sequence[SplitPageJob]):
    """Process the jobs to split pages."""
    file_count = len(jobs)
    typer.echo("\nSplitting bid packages into pages.....")
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        FileSizeColumn(),
        TotalFileSizeColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(
            f"1 of {file_count}", total=total_size_of_files(jobs=jobs)
        )
        total_pages = 0
        for idx, job in enumerate(jobs, start=1):
            pages = parse_page_lines_from_file(path_in=job.path_in)
            page_count = write_page_lines(
                file_stem=job.path_in.stem,
                pages=pages,
                path_out=job.path_out,
                overwrite=job.overwrite,
            )
            total_pages += page_count
            progress.update(
                task,
                advance=job.path_in.stat().st_size,
                description=f"{idx} of {file_count}, {total_pages} pages found.",
            )
