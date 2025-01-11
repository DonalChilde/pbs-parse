"""FILE: validation_model_from_files.py."""

import logging
from datetime import date
from pathlib import Path

from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER, ParsedTrip
from pbs_parse.pbs_2022_01.models.structured import (
    STRUCTURED_TRIP_SERIALIZER,
    StructuredTrip,
)
from pbs_parse.pbs_2022_01.models.structured_validation import StructuredValidation
from pbs_parse.snippets.datetime.date_range import date_range

logger = logging.getLogger(__name__)


def validation_model_from_objects(
    parsed_trip: ParsedTrip,
    structured_trip: StructuredTrip,
    parsed_trip_path: str = "",
    structured_trip_path: str = "",
) -> StructuredValidation:
    """validation_model_from_objects.

    Args:
        parsed_trip (ParsedTrip): _description_
        structured_trip (StructuredTrip): _description_
        parsed_trip_path (str, optional): _description_. Defaults to "".
        structured_trip_path (str, optional): _description_. Defaults to "".

    Returns:
        StructuredValidation: _description_
    """
    vm = StructuredValidation(
        parsed=parsed_trip,
        structured=structured_trip,
        parsed_path=parsed_trip_path,
        structured_path=structured_trip_path,
    )
    vm.valid_start_dates = possible_start_dates(structured_trip=structured_trip)
    return vm


def validation_model_from_files(
    parsed_trip_path: Path, structured_trip_path: Path
) -> StructuredValidation:
    """Validate_files _summary_.

    Returns:
        StructuredValidation: Will contain any error messages generated.
    """
    parsed_trip = PARSED_TRIP_SERIALIZER.load_from_json(path_in=parsed_trip_path)
    structured_trip = STRUCTURED_TRIP_SERIALIZER.load_from_json(
        path_in=structured_trip_path
    )

    vm = StructuredValidation(
        parsed=parsed_trip,
        structured=structured_trip,
        parsed_path=str(parsed_trip_path),
        structured_path=str(structured_trip_path),
    )
    vm.valid_start_dates = possible_start_dates(structured_trip=structured_trip)
    return vm


def possible_start_dates(structured_trip: StructuredTrip) -> list[date]:
    """possible_start_dates.

    Args:
        structured_trip (StructuredTrip): _description_

    Returns:
        list[date]: _description_
    """
    try:
        start_date = date.fromisoformat(structured_trip.external.effective_from)
        end_date = date.fromisoformat(structured_trip.external.effective_to)
        start_dates = list(date_range(start_date=start_date, end_date=end_date))
    except ValueError as e:
        logger.exception(
            msg=f"Unable to form date range using {structured_trip.external!r} {e}",
        )
        return []
    return start_dates
