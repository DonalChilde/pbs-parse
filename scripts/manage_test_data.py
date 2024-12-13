"""Cli to manage pbs data store. WIP."""

# ruff: noqa: D101 D102 D103
import logging
import shutil
from datetime import date, datetime
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.cli import (
    expand_trips_cli,
    parse_trips_cli,
    split_pages_cli,
    split_trips_cli,
    structure_trips_cli,
)

# typer ./scripts/manage_test_data.py run parse-source-all ~/projects/tmp/pbs-data/2024.11.01-2024.12.01 2024-11-01 2024-12-01
# typer ./scripts/manage_test_data.py run reset-source-all ~/projects/tmp/pbs-data/2024.11.01-2024.12.01

# typer ./scripts/manage_test_data.py run expand-all ~/projects/tmp/pbs-data/2024.11.01-2024.12.01
# typer ./scripts/manage_test_data.py run reset-expanded-all ~/projects/tmp/pbs-data/2024.11.01-2024.12.01

app = typer.Typer()
logger = logging.getLogger(__name__)


def get_text_source_files(path_in: Path) -> list[Path]:
    """Get the path for each .txt file in a directory.

    Data store layout assumes each bidding period is contained
    by a separate directory, and each .txt file is a bid package
    for a base in that bidding period.
    """
    return list(path_in.glob("*.txt"))


def output_base_dir_from_source_file(source_path: Path) -> Path:
    """Get the path to a directory based on the file name and path given.

    Data store layout assumes a subdirectory based on the name of the source
    file, without the file suffix, in the same directory as the source file.
    """
    return source_path.parent / source_path.stem


def parsed_trip_dir_from_source_file(source_file: Path) -> Path:
    """Get the directory for parsed trips, based on the source .txt file."""
    base_dir = output_base_dir_from_source_file(source_file)
    return base_dir / "parsed"


def expanded_trip_dir_from_source_file(source_file: Path) -> Path:
    """Get the directory for expanded trips, base on the source .txt file."""
    base_dir = output_base_dir_from_source_file(source_file)
    return base_dir / "expanded"


def structured_trip_dir_from_source_file(source_file: Path) -> Path:
    """Get the directory for structured trips, based on the source .txt file."""
    base_dir = output_base_dir_from_source_file(source_file)
    return base_dir / "structured"


def split_trip_dir_from_source_path(source_file: Path) -> Path:
    """Get the directory for split trips, based on the source .txt file."""
    base_dir = output_base_dir_from_source_file(source_file)
    return base_dir / "split_trips"


def split_page_dir_from_source_file(source_file: Path) -> Path:
    """Get the directory for split pages, based on the source .txt file."""
    base_dir = output_base_dir_from_source_file(source_file)
    return base_dir / "split_pages"


def remove_expanded_trip_directory(source_file: Path):
    """Remove the expanded trip directory, based on the source .txt file."""
    structured_dir = expanded_trip_dir_from_source_file(source_file)
    if structured_dir.is_dir():
        shutil.rmtree(structured_dir)


def remove_structured_trip_directory(source_file_path: Path):
    """Remove the structured trip directory, based on the source .txt file."""
    structured_dir = structured_trip_dir_from_source_file(source_file_path)
    if structured_dir.is_dir():
        shutil.rmtree(structured_dir)


def remove_parsed_trip_directory(source_file_path: Path):
    """Remove the parsed trip directory, based on the source .txt file."""
    parsed_dir = parsed_trip_dir_from_source_file(source_file_path)
    if parsed_dir.is_dir():
        shutil.rmtree(parsed_dir)


def remove_split_trip_directory(source_file_path: Path):
    """Remove the split trip directory, based on the source .txt file."""
    parsed_dir = split_trip_dir_from_source_path(source_file_path)
    if parsed_dir.is_dir():
        shutil.rmtree(parsed_dir)


def remove_split_page_directory(source_file_path: Path):
    """Remove the split page directory, based on the source .txt file."""
    parsed_dir = split_page_dir_from_source_file(source_file_path)
    if parsed_dir.is_dir():
        shutil.rmtree(parsed_dir)


def remove_output_directory(source_file_path: Path):
    """Remove a data directory, based on the source .txt file.

    This removes entire parsed/split data directory, not just the data for individual
    parse steps.
    """
    parsed_dir = output_base_dir_from_source_file(source_file_path)
    if parsed_dir.is_dir():
        shutil.rmtree(parsed_dir)


def expand_trips(source_path: Path, overwrite: bool):
    """Expand structured trips base on the source .txt file."""
    jobs = expand_trips_cli.build_jobs_from_directory(
        path_in=structured_trip_dir_from_source_file(source_path),
        path_out=expanded_trip_dir_from_source_file(source_path),
        overwrite=overwrite,
    )
    expand_trips_cli.expand_trips_rich(jobs=jobs)


def structure_trips(
    source_path: Path, effective_from: date, effective_to: date, overwrite: bool
):
    """Structure parsed trips based on the source .txt file."""
    jobs = structure_trips_cli.build_jobs_from_directory(
        path_in=parsed_trip_dir_from_source_file(source_path),
        path_out=structured_trip_dir_from_source_file(source_path),
        effective_from=effective_from,
        effective_to=effective_to,
        overwrite=overwrite,
    )
    structure_trips_cli.structure_trips_rich(jobs=jobs)


def parse_trips(source_path: Path, overwrite: bool):
    """Parse split trips based on the source .txt file."""
    jobs = parse_trips_cli.build_jobs_from_directory(
        path_in=split_trip_dir_from_source_path(source_path),
        path_out=parsed_trip_dir_from_source_file(source_path),
        overwrite=overwrite,
    )
    parse_trips_cli.parse_trips_rich(jobs=jobs)


def split_pages(source_path: Path, overwrite: bool):
    """Split pages based on the source .txt file."""
    job = split_pages_cli.build_job_from_file(
        path_in=source_path,
        path_out=split_page_dir_from_source_file(source_file=source_path),
        overwrite=overwrite,
    )
    jobs = [job]
    split_pages_cli.extract_pages_rich(jobs=jobs)


def split_trips(source_path: Path, overwrite: bool):
    """Split trips based on the source .txt file."""
    jobs = split_trips_cli.build_jobs_from_dir(
        path_in=split_page_dir_from_source_file(source_file=source_path),
        path_out=split_trip_dir_from_source_path(source_file=source_path),
        overwrite=overwrite,
    )
    split_trips_cli.extract_trips_rich(jobs=jobs)


# TODO get dates from parent dir name
@app.command()
def parse_source(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source txt file.", exists=True, file_okay=True, dir_okay=False
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for text file.")
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
    if path_in.suffix.lower() != ".txt":
        raise typer.BadParameter("PATH_IN is not a text file.")
    split_pages(source_path=path_in, overwrite=overwrite)
    split_trips(source_path=path_in, overwrite=overwrite)
    parse_trips(source_path=path_in, overwrite=overwrite)
    structure_trips(
        source_path=path_in,
        effective_from=effective_from.date(),
        effective_to=effective_to.date(),
        overwrite=overwrite,
    )
    expand_trips(source_path=path_in, overwrite=overwrite)


@app.command()
def parse_source_all(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Directory of source txt files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
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
    glob = "*.txt"
    typer.echo("\nParsing Bid Packages.....")
    typer.echo(f"Looking for files in {path_in}")
    files = [f for f in path_in.glob(glob) if f.is_file()]
    typer.echo(f"Found {len(files)} files")
    if not files:
        raise typer.BadParameter(
            f"No files found in directory. files are expected to match {glob}"
        )
    for file in files:
        split_pages(source_path=file, overwrite=overwrite)
    for file in files:
        split_trips(source_path=file, overwrite=overwrite)
    for file in files:
        parse_trips(source_path=file, overwrite=overwrite)
    for file in files:
        structure_trips(
            source_path=file,
            effective_from=effective_from.date(),
            effective_to=effective_to.date(),
            overwrite=overwrite,
        )
    for file in files:
        expand_trips(source_path=file, overwrite=overwrite)


@app.command()
def reset_expanded_all(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Directory of source txt files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
):
    glob = "*.txt"
    typer.echo("\nParsing Bid Packages.....")
    typer.echo(f"Looking for files in {path_in}")
    files = [f for f in path_in.glob(glob) if f.is_file()]
    typer.echo(f"Found {len(files)} files")
    if not files:
        raise typer.BadParameter(
            f"No files found in directory. files are expected to match {glob}"
        )
    for file in files:
        remove_expanded_trip_directory(source_file=file)


@app.command()
def expand_all(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Directory of source txt files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
):
    glob = "*.txt"
    typer.echo("\nParsing Bid Packages.....")
    typer.echo(f"Looking for files in {path_in}")
    files = [f for f in path_in.glob(glob) if f.is_file()]
    typer.echo(f"Found {len(files)} files")
    if not files:
        raise typer.BadParameter(
            f"No files found in directory. files are expected to match {glob}"
        )
    for file in files:
        expand_trips(source_path=file, overwrite=False)


@app.command()
def reset_source(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source txt file.", exists=True, file_okay=True, dir_okay=False
        ),
    ],
):
    remove_output_directory(source_file_path=path_in)


@app.command()
def reset_source_all(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Directory of source txt files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
):
    glob = "*.txt"
    typer.echo("\nResetting parsed Bid Packages data.....")
    typer.echo(f"Looking for files in {path_in}")
    files = [f for f in path_in.glob(glob) if f.is_file()]
    typer.echo(f"Found {len(files)} files")
    if not files:
        raise typer.BadParameter(
            f"No files found in directory. files are expected to match {glob}"
        )
    for file in files:
        remove_output_directory(source_file_path=file)
