import shutil
import subprocess
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer()
# typer ./scripts/structure_test_data.py run structure-trips ~/projects/tmp/pbs-data/2024.11.01-2024.12.01
# typer ./scripts/structure_test_data.py run reset ~/projects/tmp/pbs-data/2024.11.01-2024.12.01


def get_text_source_files(path_in: Path) -> list[Path]:
    return list(path_in.glob("*.txt"))


def output_base_dir_from_source_file(source_path: Path) -> Path:
    output_dir = source_path.parent / source_path.stem
    return output_dir


def parsed_trip_dir_from_source_file(source_file: Path) -> Path:
    parsed_dir = output_base_dir_from_source_file(source_file)
    page_dir = parsed_dir / "parsed"
    return page_dir


def structured_trip_dir_from_source_file(source_file: Path) -> Path:
    parsed_dir = output_base_dir_from_source_file(source_file)
    page_dir = parsed_dir / "structured"
    return page_dir


def remove_structured_trip_directories(source_file_paths: list[Path]):
    for file_path in source_file_paths:
        structured_dir = structured_trip_dir_from_source_file(file_path)
        if structured_dir.is_dir():
            shutil.rmtree(structured_dir)


def remove_parsed_trip_directories(source_file_paths: list[Path]):
    for file_path in source_file_paths:
        parsed_dir = parsed_trip_dir_from_source_file(file_path)
        if parsed_dir.is_dir():
            shutil.rmtree(parsed_dir)


def split_trip_dir_from_source_path(source_file: Path) -> Path:
    parsed_dir = output_base_dir_from_source_file(source_file)
    trip_dir = parsed_dir / "trip"
    return trip_dir


def structure_trips_from_files(source_paths: list[Path]):
    for source_file in source_paths:
        path_in = parsed_trip_dir_from_source_file(source_file)
        path_out = structured_trip_dir_from_source_file(source_file)
        path_out.mkdir(parents=True)
        args = [
            "pbs-parse",
            "structure",
            "trips",
            "--no-overwrite",
            f"{path_in}",
            f"{path_out}",
        ]
        result = subprocess.run(args, capture_output=True, check=True)
        typer.echo(result.stdout)
        typer.echo(result.stderr)


def parse_trips_from_files(source_paths: list[Path]):
    for source_file in source_paths:
        path_in = split_trip_dir_from_source_path(source_file)
        path_out = parsed_trip_dir_from_source_file(source_file)
        path_out.mkdir(parents=True)
        args = [
            "pbs-parse",
            "parse",
            "trips",
            "--no-overwrite",
            f"{path_in}",
            f"{path_out}",
        ]
        result = subprocess.run(args, capture_output=True, check=True)
        typer.echo(result.stdout)
        typer.echo(result.stderr)


@app.command()
def reset(
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The directory containing the source files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
):
    """
    Reset the structured trip data directories.

    Data directories are found in the same directory as the source files, and are named
    based on the Path.stem of the source file.
    """
    source_files = get_text_source_files(path_in=path_in)
    remove_structured_trip_directories(source_file_paths=source_files)
    typer.echo(f"Removed structured trip directories from {path_in}")


@app.command()
def structure_trips(
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The directory containing the source files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
):
    """translate the trips found in the `parsed` dir to the `structured` data directory."""
    source_files = get_text_source_files(path_in=path_in)
    structure_trips_from_files(source_paths=source_files)
    typer.echo(f"Structured trips for {len(source_files)} bid packages from {path_in}")
