"""Cli to translate structured to expanded trips."""

import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
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

from pbs_parse.pbs_2022_01.expand.structured_to_expanded import (
    translate_structured_trip_from_file,
)
from pbs_parse.pbs_2022_01.models.expanded import (
    EXPANDED_TRIP_SERIALIZER,
    default_file_name,
)
from pbs_parse.pbs_2022_01.validate.validate_expanded import validate_files
from pbs_parse.snippets.json.json_simple_encoder import DateTimeIsoEncoderSimple

app = typer.Typer()

import logging

logger = logging.getLogger(__name__)


@dataclass
class ExpandTripJob:
    """Job."""

    path_in: Path
    path_out: Path
    overwrite: bool = False


def total_size_of_files(jobs: Sequence[ExpandTripJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.path_in.stat().st_size
    return total


def expand_trips_rich(jobs: Sequence[ExpandTripJob]):
    """Turn structured trips into expanded trips, and save them."""
    file_count = len(jobs)
    typer.echo("Expanding structured trips.....")
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
        total_errors = 0
        trips_with_errors = 0

        for idx, job in enumerate(jobs, start=1):
            expanded_trips = translate_structured_trip_from_file(path_in=job.path_in)
            for trip in expanded_trips:
                path_out = job.path_out / default_file_name(trip=trip)
                EXPANDED_TRIP_SERIALIZER.save_as_json(
                    path_out=path_out, complex_obj=trip
                )

                validation = validate_files(
                    structured_trip_path=job.path_in, expanded_trip_path=path_out
                )
                if validation.errors:
                    error_out = path_out.parent / f"{path_out.stem}.errors.json"
                    error_out.write_text(
                        json.dumps(
                            asdict(validation), indent=1, cls=DateTimeIsoEncoderSimple
                        )
                    )
                    trips_with_errors += 1
                    total_errors += len(validation.errors)
                    progress.console.print(
                        f"Found {len(validation.errors)} errors in {job.path_out.name}"
                    )
            total_trips += 1
            progress.update(
                task,
                advance=job.path_in.stat().st_size,
                description=f"{idx} of {file_count}, {total_trips} trips found.",
            )
        if trips_with_errors > 0:
            progress.console.print(f"Found errors in {trips_with_errors} trips.")
    typer.echo("\n")


@app.command()
def trip(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source structured trip .json file.", exists=True, file_okay=True
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for expanded trips.")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
):
    """Expand the structured trip."""
    if path_in.is_dir():
        raise typer.BadParameter("PATH_IN is a directory, should be a file.")
    if path_out.is_file():
        raise typer.BadParameter("PATH_OUT is a file and should be a directory.")
    if not path_in.is_file():
        raise typer.BadParameter("PATH_IN is not a file, or it doesn't exist.")

    jobs: list[ExpandTripJob] = []
    jobs.append(
        ExpandTripJob(
            path_in=path_in,
            path_out=path_out,
            overwrite=overwrite,
        )
    )
    expand_trips_rich(jobs=jobs)


@app.command()
def all(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="directory containing structured trip .json files.",
            exists=True,
            file_okay=False,
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for expanded trip files.")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
):
    """Expand all the structured trips found in PATH_IN."""
    jobs = build_jobs_from_directory(
        path_in=path_in,
        path_out=path_out,
        overwrite=overwrite,
    )
    expand_trips_rich(jobs=jobs)


def build_jobs_from_directory(
    path_in: Path,
    path_out: Path,
    overwrite: bool,
) -> Sequence[ExpandTripJob]:
    """build_jobs_from_directory _summary_.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        overwrite (bool): _description_

    Raises:
        typer.BadParameter: _description_
        typer.BadParameter: _description_
        typer.BadParameter: _description_

    Returns:
        Sequence[ExpandTripJob]: _description_
    """
    glob = "*.structured.json*"
    files = []
    if path_in.is_file():
        raise typer.BadParameter("PATH_IN is a file and should be a directory.")
    if path_out.is_file():
        raise typer.BadParameter("PATH_OUT is a file and should be a directory.")
    if path_in.is_dir():
        typer.echo("\nCollecting structured trips.....")
        typer.echo(f"Looking for files in {path_in}")
        files = [f for f in path_in.glob(glob) if f.is_file()]
        typer.echo(f"Found {len(files)} files")
        if not files:
            raise typer.BadParameter(
                f"No files found in directory. files are expected to match {glob}"
            )
    jobs: list[ExpandTripJob] = []
    for input_file in files:
        jobs.append(
            ExpandTripJob(
                path_in=input_file,
                path_out=path_out,
                overwrite=overwrite,
            )
        )
    return jobs
