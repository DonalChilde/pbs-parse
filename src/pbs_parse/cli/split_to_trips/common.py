"""FILE: common.py."""

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

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

from pbs_parse.pbs_2022_01.split.extract_trips import (
    parse_trip_lines_from_file,
    write_trip_lines,
)

logger = logging.getLogger(__name__)
app = typer.Typer()


@dataclass
class SplitTripJob:
    """Job container."""

    split_page_path: Path
    split_trip_path: Path
    overwrite: bool = False


def build_job_from_file(path_in: Path, path_out: Path, overwrite: bool) -> SplitTripJob:
    """Check for valid inputs and return a `SplitTripJob`."""
    if path_in.is_file():
        if path_in.suffix.lower() != ".json":
            raise typer.BadParameter(
                f"Input path might not be a valid file, it does not have a .json suffix. {path_in}"
            )
    else:
        raise typer.BadParameter(f"Input path is not a valid file. {path_in}")
    if path_out.is_file():
        raise typer.BadParameter(
            f"Output path is a file, it should be a directory. {path_out}"
        )
    job = SplitTripJob(
        split_page_path=path_in, split_trip_path=path_out, overwrite=overwrite
    )
    return job


def build_jobs_from_dir(
    path_in: Path, path_out: Path, overwrite: bool
) -> Sequence[SplitTripJob]:
    """Collect text files, and use to build `SplitTripJob`s."""
    glob = "page-lines_*.json"
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


def split_to_trips_worker(jobs: Sequence[SplitTripJob]):
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
            trips = parse_trip_lines_from_file(path_in=job.split_page_path)
            trip_count = write_trip_lines(
                file_stem=job.split_page_path.stem,
                trips=trips,
                path_out=job.split_trip_path,
                overwrite=job.overwrite,
            )
            total_trips += trip_count
            progress.update(
                task,
                advance=job.split_page_path.stat().st_size,
                description=f"{idx} of {file_count}, {total_trips} trips found.",
            )


def total_size_of_files(jobs: Sequence[SplitTripJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.split_page_path.stat().st_size
    return total
