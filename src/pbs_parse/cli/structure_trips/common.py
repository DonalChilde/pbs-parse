"""FILE: common.py."""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
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

from pbs_parse.pbs_2022_01.models.structured import STRUCTURED_TRIP_SERIALIZER
from pbs_parse.pbs_2022_01.structure.parsed_to_structured import (
    structure_trip_from_file,
)
from pbs_parse.pbs_2022_01.validate.validate_structured import (
    validate_structured_trip_from_file,
)
from pbs_parse.snippets.file.check_file import check_file

app = typer.Typer()

import logging

logger = logging.getLogger(__name__)


@dataclass
class StructureTripJob:
    """Job."""

    parsed_trip_path: Path
    structured_trip_path: Path
    effective_from: date
    effective_to: date
    overwrite: bool = False


def build_jobs_from_directory(
    path_in: Path,
    path_out: Path,
    effective_from: date,
    effective_to: date,
    overwrite: bool,
) -> Sequence[StructureTripJob]:
    """build_jobs_from_directory.

    Args:
        path_in (Path): _description_
        path_out (Path): _description_
        effective_from (date): _description_
        effective_to (date): _description_
        overwrite (bool): _description_

    Raises:
        typer.BadParameter: _description_
        typer.BadParameter: _description_

    Returns:
        Sequence[StructureTripJob]: _description_
    """
    glob = "parsed-trip_*.json*"
    files = []
    if path_in.is_file():
        raise typer.BadParameter("PATH_IN is a file and should be a directory.")
    if path_in.is_dir():
        typer.echo("\nCollecting parsed trips.....")
        typer.echo(f"Looking for files in {path_in}")
        files = [f for f in path_in.glob(glob) if f.is_file()]
        typer.echo(f"Found {len(files)} files")
        if not files:
            raise typer.BadParameter(
                f"No files found in directory. files are expected to match {glob}"
            )
    jobs: list[StructureTripJob] = []
    for input_file in files:
        jobs.append(
            StructureTripJob(
                parsed_trip_path=input_file,
                structured_trip_path=path_out,
                overwrite=overwrite,
                effective_from=effective_from,
                effective_to=effective_to,
            )
        )
    return jobs


def total_size_of_files(jobs: Sequence[StructureTripJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.parsed_trip_path.stat().st_size
    return total


def structure_worker(jobs: Sequence[StructureTripJob]):
    """rich_worker.

    Args:
        jobs (Sequence[StructureTripJob]): _description_
    """
    file_count = len(jobs)
    typer.echo("Structuring parsed trips.....")
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
            structured_trip = structure_trip_from_file(
                path_in=job.parsed_trip_path,
                effective_from=job.effective_from,
                effective_to=job.effective_to,
            )
            path_out = job.structured_trip_path / structured_trip.default_file_name()
            STRUCTURED_TRIP_SERIALIZER.save_as_json(
                path_out=path_out, complex_obj=structured_trip, overwrite=job.overwrite
            )
            validation = validate_structured_trip_from_file(
                parsed_trip_path=job.parsed_trip_path, structured_trip_path=path_out
            )
            if validation.errors:
                error_out = (
                    job.structured_trip_path.parent
                    / "errors"
                    / f"{job.structured_trip_path.stem}.errors.txt"
                )
                check_file(error_out)
                error_out.write_text(str(validation))
                trips_with_errors += 1
                total_errors += len(validation.errors)
                progress.console.print(
                    f"Found {len(validation.errors)} errors in {job.structured_trip_path.name}"
                )
            total_trips += 1
            progress.update(
                task,
                advance=job.parsed_trip_path.stat().st_size,
                description=f"{idx} of {file_count}, {total_trips} trips found.",
            )
        if trips_with_errors > 0:
            progress.console.print(f"Found errors in {trips_with_errors} trips.")
    typer.echo("\n")


def default_file_name(path_in: Path) -> str:
    """default_file_name.

    Args:
        path_in (Path): _description_

    Returns:
        str: _description_
    """
    return f"{path_in.stem}.structured.json"
