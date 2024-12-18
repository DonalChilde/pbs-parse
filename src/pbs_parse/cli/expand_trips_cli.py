"""Cli to translate structured to expanded trips."""

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

from pbs_parse.pbs_2022_01.expand.structured_to_expanded_cls import StructuredToExpanded
from pbs_parse.pbs_2022_01.models.expanded import (
    EXPANDED_TRIP_SERIALIZER,
    default_file_name,
)
from pbs_parse.pbs_2022_01.models.structured import (
    STRUCTURED_TRIP_SERIALIZER,
)
from pbs_parse.pbs_2022_01.validate.expanded.validator import ExpandedValidator

app = typer.Typer()

import logging

logger = logging.getLogger(__name__)


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
            s_trip_path=path_in,
            dir_path_out=path_out,
            overwrite=overwrite,
        )
    )
    rich_worker(jobs=jobs)


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
    rich_worker(jobs=jobs)


@dataclass
class ExpandTripJob:
    """Job."""

    s_trip_path: Path
    dir_path_out: Path
    overwrite: bool = False


def total_size_of_files(jobs: Sequence[ExpandTripJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.s_trip_path.stat().st_size
    return total


def rich_worker(jobs: Sequence[ExpandTripJob]):
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
            s_trip = STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=job.s_trip_path)
            translator = StructuredToExpanded(structured_trip=s_trip)
            expanded_trips = translator.translate()
            for trip in expanded_trips:
                path_out = job.dir_path_out / default_file_name(trip=trip)
                EXPANDED_TRIP_SERIALIZER.save_as_json(
                    path_out=path_out, complex_obj=trip
                )
                validator = ExpandedValidator(
                    expanded_trip=trip,
                    structured_trip=s_trip,
                    expanded_trip_path=path_out,
                    structured_trip_path=job.s_trip_path,
                    parsed_trip_path=None,
                )
                validator.validate()
                if validator.errors:
                    error_out = (
                        path_out.parent / "errors" / f"{path_out.stem}.errors.txt"
                    )
                    error_out.write_text(str(validator))
                    trips_with_errors += 1
                    total_errors += len(validator.errors)
                    err_msg = (
                        f"Found {len(validator.errors)} errors in {path_out.name!r}"
                    )
                    progress.console.print(err_msg)
                    for msg in validator.errors:
                        progress.console.print(f"\t{msg!r}")
                    logger.warning(err_msg)
                    logger.warning("%r", validator.errors)
            total_trips += len(expanded_trips)
            progress.update(
                task,
                advance=job.s_trip_path.stat().st_size,
                description=f"{idx} of {file_count}, {total_trips} trips found.",
            )
        if trips_with_errors > 0:
            progress.console.print(f"Found errors in {trips_with_errors} trips.")
    typer.echo("\n")


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
                s_trip_path=input_file,
                dir_path_out=path_out,
                overwrite=overwrite,
            )
        )
    return jobs
