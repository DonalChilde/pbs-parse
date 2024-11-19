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

from pbs_parse.pbs_2022_01.models.structured import structured_trip_serializer
from pbs_parse.pbs_2022_01.translate.parsed_to_structured import translate_file

app = typer.Typer()


@dataclass
class StructureTripJob:
    path_in: Path
    path_out: Path
    overwrite: bool = False
    effective_from: str = ""
    effective_to: str = ""


@dataclass
class StructureTripJobs:
    jobs: list[StructureTripJob] = field(default_factory=list)

    def total_size_of_files(self) -> int:
        total = 0
        for job in self.jobs:
            total += job.path_in.stat().st_size
        return total


def structure_trips_rich(jobs: StructureTripJobs):
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
        serializer = structured_trip_serializer()
        for idx, job in enumerate(jobs.jobs, start=1):
            external_data = {
                "effective_from": job.effective_from,
                "effective_to": job.effective_to,
            }
            structured_trip = translate_file(
                path_in=job.path_in, external_data=external_data
            )
            serializer.save_as_json(
                path_out=job.path_out,
                complex_obj=structured_trip,
                overwrite=job.overwrite,
            )
            total_trips += 1
            progress.update(
                task,
                advance=job.path_in.stat().st_size,
                description=f"{idx} of {file_count}, {total_trips} trips found.",
            )


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

    jobs = StructureTripJobs()
    jobs.jobs.append(
        StructureTripJob(path_in=path_in, path_out=dest_path, overwrite=overwrite)
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
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    suppress_status_msgs: Annotated[
        bool, typer.Option(help="Suppress task status messages.")
    ] = False,
):
    glob = "*.parsed.json*"
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
    jobs = StructureTripJobs()
    for input_file in files:
        dest_path = path_out / f"{output_file_name(path_in=input_file)}"
        jobs.jobs.append(
            StructureTripJob(
                path_in=input_file, path_out=dest_path, overwrite=overwrite
            )
        )
    structure_trips_rich(jobs=jobs)
