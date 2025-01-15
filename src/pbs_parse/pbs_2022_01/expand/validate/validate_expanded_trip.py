"""FILE: validate_expanded_trip.py."""

from pbs_parse.pbs_2022_01.expand.validate.check_localized_times import (
    check_localized_times,
)
from pbs_parse.pbs_2022_01.models.expanded_validation import ExpandedValidation


def validate_expanded_trip(vm: ExpandedValidation):
    """validate_expanded_trip.

    Args:
        vm (ExpandedValidation): _description_
    """
    check_localized_times(vm=vm)
