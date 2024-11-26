"""Cli to translate split to parsed trips."""

# ruff: noqa: D101 D102 D103
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

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
    ParsedTrip,
    default_file_name,
    parsed_trip_serializer,
)
from pbs_parse.pbs_2022_01.parser.trip_lines_parser import TripLinesParser

logger = logging.getLogger(__name__)
app = typer.Typer()


@dataclass
class ParseTripJob:
    path_in: Path
    path_out: Path
    overwrite: bool = False


def total_size_of_files(jobs: Sequence[ParseTripJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.path_in.stat().st_size
    return total


def parse_trips_rich(jobs: Sequence[ParseTripJob]):
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
        serializer = parsed_trip_serializer()

        for idx, job in enumerate(jobs, start=1):
            ctx = ParseContext()
            parsed_trip = parser.parse_file(ctx=ctx, path_in=job.path_in)
            if check_for_prior_month(parsed_trip=parsed_trip):
                output_path = (
                    job.path_out.parent / job.path_out.stem / ".prior_month.json"
                )
                prior_trips += 1
            else:
                output_path = job.path_out
            serializer.save_as_json(
                path_out=output_path, complex_obj=parsed_trip, overwrite=job.overwrite
            )
            total_trips += 1
            progress.update(
                task,
                advance=job.path_in.stat().st_size,
                description=f"{idx} of {file_count}, {total_trips} trips found, with {prior_trips} prior month trips.",
            )


def check_for_prior_month(parsed_trip: ParsedTrip) -> bool:
    for line in parsed_trip.parsed_lines:
        if "trip_header" == line.id:
            if "prior" in line.indexed_string.txt:
                return True
    return False


@app.command()
def trip(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source IndexedStrings.json file.", exists=True, file_okay=True
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for parsed trip.")
    ],
    file_name: Annotated[
        Path | None,
        typer.Option(help="file name for output if differrent from default."),
    ] = None,
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
):
    if path_in.is_dir():
        raise typer.BadParameter("PATH_IN is a directory, should be a file.")
    if not path_in.is_file():
        raise typer.BadParameter("PATH_IN is not a file, or it doesn't exist.")
    if file_name is not None:
        dest_path = path_out / file_name
    else:
        dest_path = path_out / default_file_name(path_name=path_in.name)

    jobs: Sequence[ParseTripJob] = []
    jobs.append(ParseTripJob(path_in=path_in, path_out=dest_path, overwrite=overwrite))
    parse_trips_rich(jobs=jobs)


@app.command()
def trips(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Directory of trip lines files.", exists=True, file_okay=False
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="Destination directory for parsed trips.")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
):
    jobs = build_jobs_from_directory(
        path_in=path_in, path_out=path_out, overwrite=overwrite
    )
    parse_trips_rich(jobs=jobs)


def build_jobs_from_directory(
    path_in: Path,
    path_out: Path,
    overwrite: bool,
) -> Sequence[ParseTripJob]:
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
            ParseTripJob(path_in=input_file, path_out=dest_path, overwrite=overwrite)
        )
    return jobs
