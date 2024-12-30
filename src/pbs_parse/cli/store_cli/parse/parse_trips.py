"""FILE: parse_trips.py."""

from pfmsoft.state_parser import ParseContext
from rich.progress import TaskID

from pbs_parse.pbs_2022_01.models import manifest
from pbs_parse.pbs_2022_01.models.parsed_trip import (
    ParsedTrip,
)
from pbs_parse.pbs_2022_01.parse.trip_lines_parser import TripLinesParser
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

from .progress import progress


def parse_trips(
    base: str, store: StoreManager, task_id: TaskID, overwrite: bool = False
):
    """Parse and save TripLines.

    Args:
        base (str): _description_
        store (StoreManager): _description_
        task_id (TaskID): _description_
        overwrite (bool, optional): _description_. Defaults to False.
    """
    trip_infos = store.get_files_by_type(
        base=base, file_type=manifest.FileTypes.SPLIT_TRIP
    )
    total_trips = len(trip_infos)
    progress.update(task_id=task_id, total=total_trips, description="Parsing trips....")
    prior_trips = 0
    parser = TripLinesParser()
    for page_info in trip_infos:
        path_in = store.manifest_directory / page_info["file_path"]
        ctx = ParseContext()
        parsed = parser.parse_file(ctx=ctx, path_in=path_in)
        if check_for_prior_month(parsed_trip=parsed):
            store.save_parsed_prior_month_trip(
                base=base, parsed=parsed, overwrite=overwrite
            )
            prior_trips += 1
        else:
            store.save_parsed_trip(base=base, parsed=parsed, overwrite=overwrite)
        progress.update(
            task_id,
            advance=1,
            # description=f"{prior_trips} prior month trips found.",
        )


def check_for_prior_month(parsed_trip: ParsedTrip) -> bool:
    """Check to see if the trip is a `prior month` trip."""
    for line in parsed_trip.parsed_lines:
        if "trip_header" == line.id:
            if "prior" in line.indexed_string.txt:
                return True
    return False
