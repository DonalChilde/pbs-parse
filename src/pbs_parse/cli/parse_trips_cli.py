from dataclasses import dataclass, field
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

from pbs_parse.pbs_2022_01.parser.parse import TripParser
from pbs_parse.snippets.indexed_string.state_parser.parse_context import ParseContext

app = typer.Typer()


@dataclass
class ParseTripJob:
    path_in: Path
    path_out: Path
    overwrite: bool = False


@dataclass
class ParseTripJobs:
    jobs: list[ParseTripJob] = field(default_factory=list)

    def total_size_of_files(self) -> int:
        total = 0
        for job in self.jobs:
            total += job.path_in.stat().st_size
        return total


def parse_trips_rich(jobs: ParseTripJobs):
    file_count = len(jobs.jobs)
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        FileSizeColumn(),
        TotalFileSizeColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(f"1 of {file_count}", total=jobs.total_size_of_files())
        total_trips = 0
        parser = TripParser()
        for idx, job in enumerate(jobs.jobs, start=1):
            ctx = ParseContext()
            parsed = parser.parse_file(ctx=ctx, path_in=job.path_in)
            parsed.to_file(path_out=job.path_out, overwrite=job.overwrite)
            total_trips += 1
            progress.update(
                task,
                advance=job.path_in.stat().st_size,
                description=f"{idx} of {file_count}, {total_trips} trips found.",
            )


def output_file_name(path_in: Path) -> str:
    return f"{path_in.stem}.parsed.json"


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
        dest_path = path_out / f"{output_file_name(path_in=path_in)}"

    jobs = ParseTripJobs()
    jobs.jobs.append(
        ParseTripJob(path_in=path_in, path_out=dest_path, overwrite=overwrite)
    )
    parse_trips_rich(jobs=jobs)


@app.command()
def trips(
    ctx: typer.Context,
    path_in: Annotated[
        Path, typer.Argument(help="source pdf file.", exists=True, file_okay=False)
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for text file.")
    ],
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
):
    glob = "*.trip_*"
    files = []
    if path_in.is_file():
        raise typer.BadParameter("PATH_IN is a file and should be a directory.")
    if path_in.is_dir():
        typer.echo(f"Looking for files in {path_in}")
        files = [f for f in path_in.glob(glob) if f.is_file()]
        typer.echo(f"Found {len(files)} files")
        if not files:
            raise typer.BadParameter(
                f"No files found in directory. files are expected to match {glob}"
            )
    jobs = ParseTripJobs()
    for input_file in files:
        dest_path = path_out / f"{output_file_name(path_in=input_file)}"
        jobs.jobs.append(
            ParseTripJob(path_in=input_file, path_out=dest_path, overwrite=overwrite)
        )
    parse_trips_rich(jobs=jobs)
