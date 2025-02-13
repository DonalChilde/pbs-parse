"""Tests for cli, parse trips."""

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner
from whenever import Date

from pbs_parse.cli.main_typer import app
from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.models.bid_data import BidData, Effective
from tests.pbs_parse.pbs_2022_01.cli import BID_PACKAGE


def test_parse_trips(test_output_dir: Path):
    """test_parse_trips.

    Args:
        runner (CliRunner): _description_
        test_output_dir (Path): _description_
    """
    pages_out = test_output_dir / "cli-manual" / "parse-trips" / "pages"
    trips_out = test_output_dir / "cli-manual" / "parse-trips" / "trips"
    parsed_out = test_output_dir / "cli-manual" / "parse-trips" / "parsed"
    effective = Effective(start=Date(2024, 11, 1), end=Date(2024, 12, 1))
    bid_data = BidData(name="2024-11", base="LAX", effective=effective)
    with resources.as_file(BID_PACKAGE.traversable()) as input_path:
        pages = list(API.transform.source_to_pages(path_in=input_path, bid=bid_data))
    for page in pages:
        API.save.page_lines(dir_out=pages_out, page_lines=page)
    trips = list(API.transform.pages_to_trips(pages=pages))
    for trip in trips:
        API.save.trip_lines(dir_out=trips_out, trip_lines=trip)
    result = CliRunner().invoke(
        app,
        [
            "manual",
            "parse-trips",
            str(trips_out),
            str(parsed_out),
        ],
    )
    if result.stderr_bytes is not None:
        print(result.stderr)
    print(result.stdout)
    assert result.exit_code == 0
    # assert "18/18" in result.stdout
    # assert "error" not in result.stdout
    result_files = list(parsed_out.glob("parsed-trip*"))
    assert len(result_files) == 18
