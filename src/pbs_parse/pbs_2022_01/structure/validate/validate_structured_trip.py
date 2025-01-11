"""FILE: validate_structured_trip.py."""

from pbs_parse.pbs_2022_01.models.structured_validation import StructuredValidation
from pbs_parse.pbs_2022_01.structure.validate.calendar_starts_count import (
    calendar_starts_count,
)


def validate_structured_trip(
    vm: StructuredValidation,
) -> StructuredValidation:
    """validate_structured_trip.

    Args:
        vm (StructuredValidation): _description_

    Returns:
        StructuredValidation: _description_
    """
    calendar_starts_count(vm=vm)
    return vm
