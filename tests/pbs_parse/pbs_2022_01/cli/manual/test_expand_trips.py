"""Tests for cli, expand trips."""

import logging
from importlib import resources
from pathlib import Path

import pytest
from typer.testing import CliRunner
from whenever import Date

from pbs_parse.cli.main_typer import app
from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.models.bid_data import BidData, Effective
from tests.pbs_parse.pbs_2022_01.cli import BID_PACKAGE


def test_expand_trips(test_output_dir: Path, caplog: pytest.LogCaptureFixture):
    """test_parse_trips.

    Args:
        runner (CliRunner): _description_
        test_output_dir (Path): _description_
        caplog (pytest.LogCaptureFixture): _description_
    """
    caplog.set_level(logging.WARNING)
    pages_out = test_output_dir / "cli-manual" / "expand-trips" / "pages"
    trips_out = test_output_dir / "cli-manual" / "expand-trips" / "trips"
    parsed_out = test_output_dir / "cli-manual" / "expand-trips" / "parsed"
    expanded_out = test_output_dir / "cli-manual" / "expand-trips" / "expanded"
    effective = Effective(start=Date(2024, 11, 1), end=Date(2024, 12, 1))
    bid_data = BidData(name="2024-11", base="LAX", effective=effective)
    with resources.as_file(BID_PACKAGE.traversable()) as input_path:
        pages = list(API.transform.source_to_pages(path_in=input_path, bid=bid_data))
    for page in pages:
        API.save.page_lines(dir_out=pages_out, page_lines=page)
    trips = list(API.transform.pages_to_trips(pages=pages))
    for trip in trips:
        API.save.trip_lines(dir_out=trips_out, trip_lines=trip)
    parsed_trips = API.transform.trips_to_parsed(trips=trips)
    for parsed_trip in parsed_trips:
        API.save.parsed_trip(dir_out=parsed_out, parsed_trip=parsed_trip)

    result_1 = CliRunner().invoke(
        app,
        [
            "manual",
            "expand-trips",
            str(parsed_out),
            str(expanded_out),
        ],
    )
    if result_1.stderr_bytes is not None:
        print(result_1.stderr)
    print(result_1.stdout)
    assert result_1.exit_code == 0
    assert "2 expanded trips with errors" in result_1.stdout
    result_files = list(expanded_out.glob("expanded-trip*"))
    assert len(result_files) == 83
