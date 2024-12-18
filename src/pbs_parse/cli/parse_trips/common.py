"""FILE: common.py."""

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import typer
from pfmsoft.state_parser import ParseContext
from rich.progress import (
    BarColumn,
    FileSizeColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TotalFileSizeColumn,
)

from pbs_parse.pbs_2022_01.models.parsed_trip import (
    PARSED_TRIP_SERIALIZER,
    ParsedTrip,
    default_file_name,
)
from pbs_parse.pbs_2022_01.parse.trip_lines_parser import TripLinesParser

logger = logging.getLogger(__name__)


@dataclass
class ParseTripJob:
    """Job."""

    split_trip_path: Path
    parsed_trip_path: Path
    overwrite: bool = False


def build_jobs_from_directory(
    path_in: Path,
    path_out: Path,
    overwrite: bool,
) -> Sequence[ParseTripJob]:
    """build_jobs_from_directory.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        overwrite (bool): _description_

    Raises:
        typer.BadParameter: _description_
        typer.BadParameter: _description_

    Returns:
        Sequence[ParseTripJob]: _description_
    """
    glob = "*.trip_*"
    files = []
    if path_in.is_file():
        raise typer.BadParameter("PATH_IN is a file and should be a directory.")
    if path_in.is_dir():
        typer.echo("\nCollecting split trips.....")
        typer.echo(f"Looking for files in {path_in}")
        files = [f for f in path_in.glob(glob) if f.is_file()]
        typer.echo(f"Found {len(files)} files")
        if not files:
            raise typer.BadParameter(
                f"No files found in directory. files are expected to match {glob}"
            )
    jobs: Sequence[ParseTripJob] = []
    for input_file in files:
        dest_path = path_out / default_file_name(path_name=input_file.name)
        jobs.append(
            ParseTripJob(
                split_trip_path=input_file,
                parsed_trip_path=dest_path,
                overwrite=overwrite,
            )
        )
    return jobs


def total_size_of_files(jobs: Sequence[ParseTripJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.split_trip_path.stat().st_size
    return total


def parse_worker(jobs: Sequence[ParseTripJob]):
    """Do the jobs, with rich output."""
    file_count = len(jobs)
    typer.echo("Parsing split trips.....")
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
        prior_trips = 0
        parser = TripLinesParser()

        for idx, job in enumerate(jobs, start=1):
            ctx = ParseContext()
            parsed_trip = parser.parse_file(ctx=ctx, path_in=job.split_trip_path)
            if check_for_prior_month(parsed_trip=parsed_trip):
                output_path = (
                    job.parsed_trip_path.parent
                    / job.parsed_trip_path.stem
                    / ".prior_month.json"
                )
                prior_trips += 1
            else:
                output_path = job.parsed_trip_path
            PARSED_TRIP_SERIALIZER.save_as_json(
                path_out=output_path, complex_obj=parsed_trip, overwrite=job.overwrite
            )
            total_trips += 1
            progress.update(
                task,
                advance=job.split_trip_path.stat().st_size,
                description=f"{idx} of {file_count}, {total_trips} trips found, with {prior_trips} prior month trips.",
            )


def check_for_prior_month(parsed_trip: ParsedTrip) -> bool:
    """Check to see if the trip is a `prior month` trip."""
    for line in parsed_trip.parsed_lines:
        if "trip_header" == line.id:
            if "prior" in line.indexed_string.txt:
                return True
    return False
