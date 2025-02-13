"""Tests for cli, split pages to trips."""

from importlib import resources
from pathlib import Path

from typer.testing import CliRunner
from whenever import Date

from pbs_parse.cli.main_typer import app
from pbs_parse.pbs_2022_01 import api as API
from pbs_parse.pbs_2022_01.models.bid_data import BidData, Effective
from tests.pbs_parse.pbs_2022_01.cli import BID_PACKAGE


def test_split_pages_to_trips(test_output_dir: Path):
    """test_split_pages_to_trips.

    Args:
        runner (CliRunner): _description_
        test_output_dir (Path): _description_
    """
    pages_out = test_output_dir / "cli-manual" / "pages-to-trips" / "pages"
    trips_out = test_output_dir / "cli-manual" / "pages-to-trips" / "trips"
    effective = Effective(start=Date(2024, 11, 1), end=Date(2024, 12, 1))
    bid_data = BidData(name="2024-11", base="LAX", effective=effective)
    with resources.as_file(BID_PACKAGE.traversable()) as input_path:
        for page in API.transform.source_to_pages(path_in=input_path, bid=bid_data):
            API.save.page_lines(dir_out=pages_out, page_lines=page)

    result = CliRunner().invoke(
        app,
        [
            "manual",
            "pages-to-trips",
            str(pages_out),
            str(trips_out),
        ],
    )
    if result.stderr_bytes is not None:
        print(result.stderr)
    print(result.stdout)
    assert result.exit_code == 0
    # assert "18/4" in result.stdout
    # assert "error" not in result.stdout
    result_files = list(trips_out.glob("trip-lines*"))
    assert len(result_files) == 18
