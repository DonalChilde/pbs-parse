"""Script to generate or regenerate test data."""

from datetime import date
from pathlib import Path

import typer

from pbs_parse.cli import (
    parse_trips_cli,
    split_pages_cli,
    split_trips_cli,
    structure_trips_cli,
)

app = typer.Typer()
RESOURCES_PATH = Path(__file__).parent
BIDPACKAGE_PATH = RESOURCES_PATH / "bid_package"
PAGELINES_PATH = RESOURCES_PATH / "page_lines"
TRIPLINES_PATH = RESOURCES_PATH / "trip_lines"
PARSEDTRIPS_PATH = RESOURCES_PATH / "parsed_trips"
STRUCTUREDTRIPS_PATH = RESOURCES_PATH / "structured_trips"


def split_bid_packages_to_pages():
    """Split the bid packages into pages."""
    eff_dates = ["2024-11-01_2024-12-01"]
    for eff_date in eff_dates:
        output_path = PAGELINES_PATH / eff_date
        files = BIDPACKAGE_PATH.glob("*.txt")
        jobs: list[split_pages_cli.SplitPageJob] = []
        for file in files:
            job = split_pages_cli.SplitPageJob(
                path_in=file, path_out=output_path, overwrite=True
            )
            jobs.append(job)
        split_pages_cli.extract_pages_rich(jobs=jobs)


def split_pages_to_trips():
    """Split the pages into trips."""
    eff_dates = ["2024-11-01_2024-12-01"]
    for eff_date in eff_dates:
        output_path = TRIPLINES_PATH / eff_date
        jobs = split_trips_cli.build_jobs_from_dir(
            path_in=PAGELINES_PATH / eff_date, path_out=output_path, overwrite=True
        )
        split_trips_cli.extract_trips_rich(jobs=jobs)


def parse_trips():
    """Parse the split trips."""
    eff_dates = ["2024-11-01_2024-12-01"]
    for eff_date in eff_dates:
        output_path = TRIPLINES_PATH / eff_date
        jobs = parse_trips_cli.build_jobs_from_directory(
            path_in=TRIPLINES_PATH / eff_date, path_out=output_path, overwrite=True
        )
        parse_trips_cli.parse_trips_rich(jobs=jobs)


def structure_parsed_trips():
    """Structure the parsed trips."""
    eff_dates = ["2024-11-01_2024-12-01"]
    for eff_date in eff_dates:
        split_dates = eff_date.split("_")
        jobs = structure_trips_cli.build_jobs_from_directory(
            path_in=PARSEDTRIPS_PATH / eff_date,
            path_out=STRUCTUREDTRIPS_PATH / eff_date,
            effective_from=date.fromisoformat(split_dates[0]),
            effective_to=date.fromisoformat(split_dates[1]),
            overwrite=True,
        )
        structure_trips_cli.structure_trips_rich(jobs=jobs)


@app.command()
def reset_data():
    """Reset all test data."""
    split_bid_packages_to_pages()
    split_pages_to_trips()
    parse_trips()
    structure_parsed_trips()


@app.command()
def stub():
    """Stub command."""


if __name__ == "__main__":
    app()
