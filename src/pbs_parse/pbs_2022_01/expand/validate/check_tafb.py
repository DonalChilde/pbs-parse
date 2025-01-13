"""FILE: check_tafb.py."""

from pbs_parse.pbs_2022_01.models.expanded_validation import ExpandedValidation


def check_tafb(vm: ExpandedValidation) -> None:
    """check_tafb.

    Args:
        vm (ExpandedValidation): _description_
    """
    expanded_tafb = vm.expanded.tafb
    structured_tafb = vm.structured.tafb
