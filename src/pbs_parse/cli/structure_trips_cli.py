from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime
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

from pbs_parse.pbs_2022_01.models.structured import structured_trip_serializer
from pbs_parse.pbs_2022_01.translate.parsed_to_structured import translate_file
from pbs_parse.pbs_2022_01.validate.validate_structured import validate_files

app = typer.Typer()

import logging

logger = logging.getLogger(__name__)


@dataclass
class StructureTripJob:
    path_in: Path
    path_out: Path
    effective_from: date
    effective_to: date
    overwrite: bool = False


def total_size_of_files(jobs: Sequence[StructureTripJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.path_in.stat().st_size
    return total


def structure_trips_rich(jobs: Sequence[StructureTripJob]):
    file_count = len(jobs)
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
        serializer = structured_trip_serializer()

        for idx, job in enumerate(jobs, start=1):
            structured_trip = translate_file(
                path_in=job.path_in,
                effective_from=job.effective_from,
                effective_to=job.effective_to,
            )
            serializer.save_as_json(
                path_out=job.path_out,
                complex_obj=structured_trip,
                overwrite=job.overwrite,
            )
            trans_ctx = validate_files(
                parsed_trip_path=job.path_in, structured_trip_path=job.path_out
            )
            if trans_ctx.errors:
                error_out = job.path_out.parent / f"{job.path_out.stem}.errors.txt"
                error_out.write_text(str(trans_ctx))
                trips_with_errors += 1
                total_errors += len(trans_ctx.errors)
                progress.console.print(
                    f"Found {len(trans_ctx.errors)} errors in {job.path_out.name}"
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


def output_file_name(path_in: Path) -> str:
    return f"{path_in.stem}.structured.json"


@app.command()
def trip(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source parsed trip .json file.", exists=True, file_okay=True
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for structured trip.")
    ],
    effective_from: Annotated[
        datetime, typer.Argument(help="Effective From date for bid package.")
    ],
    effective_to: Annotated[
        datetime, typer.Argument(help="Effective To date for bid package")
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
        dest_path = path_out / f"{output_file_name(path_in=path_in)}"

    jobs: list[StructureTripJob] = []
    jobs.append(
        StructureTripJob(
            path_in=path_in,
            path_out=dest_path,
            overwrite=overwrite,
            effective_from=effective_from.date(),
            effective_to=effective_to.date(),
        )
    )
    structure_trips_rich(jobs=jobs)


@app.command()
def trips(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="directory containing parsed trip .json files.",
            exists=True,
            file_okay=False,
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for structured trips files.")
    ],
    effective_from: Annotated[
        datetime, typer.Argument(help="Effective From date for bid package.")
    ],
    effective_to: Annotated[
        datetime, typer.Argument(help="Effective To date for bid package")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
):
    jobs = build_jobs_from_directory(
        path_in=path_in,
        path_out=path_out,
        effective_from=effective_from.date(),
        effective_to=effective_to.date(),
        overwrite=overwrite,
    )
    structure_trips_rich(jobs=jobs)


def build_jobs_from_directory(
    path_in: Path,
    path_out: Path,
    effective_from: date,
    effective_to: date,
    overwrite: bool,
) -> Sequence[StructureTripJob]:
    glob = "*.parsed.json*"
    files = []
    if path_in.is_file():
        raise typer.BadParameter("PATH_IN is a file and should be a directory.")
    if path_in.is_dir():
        typer.echo("\nStructuring Trips.....")
        typer.echo(f"Looking for files in {path_in}")
        files = [f for f in path_in.glob(glob) if f.is_file()]
        typer.echo(f"Found {len(files)} files")
        if not files:
            raise typer.BadParameter(
                f"No files found in directory. files are expected to match {glob}"
            )
    jobs: list[StructureTripJob] = []
    for input_file in files:
        dest_path = path_out / f"{output_file_name(path_in=input_file)}"
        jobs.append(
            StructureTripJob(
                path_in=input_file,
                path_out=dest_path,
                overwrite=overwrite,
                effective_from=effective_from,
                effective_to=effective_to,
            )
        )
    return jobs
