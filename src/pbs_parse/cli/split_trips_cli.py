"""Typer cli to split pages into trips."""

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

from pbs_parse.pbs_2022_01.split.extract_trips import parse_trips_from_file, write_trips

logger = logging.getLogger(__name__)
app = typer.Typer()


@dataclass
class SplitTripJob:
    """Job container."""

    path_in: Path
    path_out: Path
    overwrite: bool = False


def total_size_of_files(jobs: Sequence[SplitTripJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.path_in.stat().st_size
    return total


@app.command()
def trip(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Json file representing a page from a bid package.",
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
    """Split a page into trips."""
    _ = ctx
    job = build_job_from_file(path_in=path_in, path_out=path_out, overwrite=overwrite)
    jobs = [job]
    extract_trips_rich(jobs=jobs)


@app.command()
def all(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="A directory containing json files representing trips from a bid package.",
            exists=True,
            file_okay=False,
            dir_okay=True,
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
    """Split all the pages found in a directory into trips."""
    _ = ctx
    jobs = build_jobs_from_dir(path_in=path_in, path_out=path_out, overwrite=overwrite)
    extract_trips_rich(jobs=jobs)


def build_job_from_file(path_in: Path, path_out: Path, overwrite: bool) -> SplitTripJob:
    """Check for valid inputs and return a `SplitTripJob`."""
    if path_in.is_file():
        if path_in.suffix.lower() != ".json":
            raise typer.echo(
                f"Input path might not be a valid file, it does not have a .json suffix. {path_in}"
            )
    else:
        raise typer.BadParameter(f"Input path is not a valid file. {path_in}")
    if path_out.is_file():
        raise typer.BadParameter(
            f"Output path is a file, it should be a directory. {path_out}"
        )
    job = SplitTripJob(path_in=path_in, path_out=path_out, overwrite=overwrite)
    return job


def build_jobs_from_dir(
    path_in: Path, path_out: Path, overwrite: bool
) -> Sequence[SplitTripJob]:
    """Collect text files, and use to build `SplitTripJob`s."""
    glob = "*.page_*.json"
    if not path_in.is_dir():
        raise typer.BadParameter("PATH_IN should be a directory.")
    typer.echo("\nCollecting split pages.......")
    typer.echo(f"Looking for files in {path_in}")
    files = [f for f in path_in.glob(glob, case_sensitive=False) if f.is_file()]
    typer.echo(f"Found {len(files)} files")
    if len(files) == 0:
        raise typer.BadParameter(
            "Input path is not a directory containing valid files.\n"
            f"Files are expected to match {glob}"
        )
    jobs: list[SplitTripJob] = []
    for file in files:
        job = build_job_from_file(path_in=file, path_out=path_out, overwrite=overwrite)
        jobs.append(job)
    return jobs


# def collect_jobs(
#     path_in: Path, path_out: Path, overwrite: bool
# ) -> Sequence[SplitTripJob]:
#     """Build a collections of jobs to do."""
#     if path_in.is_dir():
#         typer.echo(f"Looking for files in {path_in}")
#         files = [f for f in path_in.glob("*.page_*") if f.is_file()]
#         typer.echo(f"Found {len(files)} files")
#         # input_paths.extend(files)
#     elif path_in.is_file():
#         files = [path_in]
#     else:
#         raise typer.BadParameter(
#             "Input path is not a valid file, or directory containing valid files.\n"
#             "Files are expected to match *.page_*"
#         )
#     typer.echo(f"Searching {len(files)} files for trips.")
#     jobs: list[SplitTripJob] = []
#     for file in files:
#         jobs.append(SplitTripJob(path_in=file, path_out=path_out, overwrite=overwrite))
#     return jobs


def extract_trips_rich(jobs: Sequence[SplitTripJob]):
    """Process the jobs to split trips."""
    file_count = len(jobs)
    typer.echo("Splitting pages into trips.....")
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
        total_trips = 0
        for idx, job in enumerate(jobs, start=1):
            trips = parse_trips_from_file(path_in=job.path_in)
            trip_count = write_trips(
                file_stem=job.path_in.stem,
                trips=trips,
                path_out=job.path_out,
                overwrite=job.overwrite,
            )
            total_trips += trip_count
            progress.update(
                task,
                advance=job.path_in.stat().st_size,
                description=f"{idx} of {file_count}, {total_trips} trips found.",
            )
