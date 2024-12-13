"""Validate expanded trips."""

import logging
from pathlib import Path

from pbs_parse.pbs_2022_01.models import expanded as ET
from pbs_parse.pbs_2022_01.models import structured as ST
from pbs_parse.pbs_2022_01.models.validation import ExpandedValidation

logger = logging.getLogger(__name__)


def validate(ctx: ExpandedValidation) -> ExpandedValidation:
    """validate.

    Args:
        ctx (ExpandedValidation): _description_

    Returns:
        ExpandedValidation: Will contain any error messages generated.
    """
    _validate(ctx=ctx)
    return ctx


def validate_files(
    expanded_trip_path: Path, structured_trip_path: Path
) -> ExpandedValidation:
    """Validate_files _summary_.

    Returns:
        StructuredValidation: Will contain any error messages generated.
    """
    expanded_trip = ET.EXPANDED_TRIP_SERIALIZER.load_from_json(
        path_in=expanded_trip_path
    )
    structured_trip = ST.STRUCTURED_TRIP_SERIALIZER.load_from_json(
        path_in=structured_trip_path
    )

    ctx = ExpandedValidation(
        expanded_trip=expanded_trip,
        structured_trip=structured_trip,
        expanded_path=str(expanded_trip_path),
        structured_path=str(structured_trip_path),
    )
    _validate(ctx=ctx)
    return ctx


def _validate(ctx: ExpandedValidation) -> None:
    """Validator functions called from here."""
    return None
