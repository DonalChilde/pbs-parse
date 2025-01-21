"""FILE: check_tafb.py."""

from datetime import timedelta

from pbs_parse.pbs_2022_01.models.expanded_validation import ExpandedValidation


def check_tafb(vm: ExpandedValidation) -> None:
    """check_tafb.

    Args:
        vm (ExpandedValidation): _description_
    """
    expanded_tafb = vm.expanded.tafb
    structured_tafb = vm.structured.tafb
    hours, minutes = structured_tafb.split(".", maxsplit=1)
    if expanded_tafb != timedelta(hours=int(hours), minutes=int(minutes)):
        msg = f"Expanded TAFB does not match structured TAFB for trip. {expanded_tafb=!s} {structured_tafb=!r}"
        vm.expanded.errors.append(msg)
