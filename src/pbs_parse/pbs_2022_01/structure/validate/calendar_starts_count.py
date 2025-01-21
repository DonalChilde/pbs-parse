"""FILE: calendar_starts_count.py."""

from pbs_parse.pbs_2022_01.models.structured_validation import StructuredValidation


def calendar_starts_count(vm: StructuredValidation) -> None:
    """Check if whole calendar was captured."""
    if len(vm.structured.calendar) != len(vm.valid_start_dates):
        msg = (
            f"len(ctx.structured_trip.calendar) != len(ctx.external_start_dates)\n"
            f"\t{len(vm.structured.calendar)} != {len(vm.valid_start_dates)}\n"
            f"\tctx.structured_trip.calendar -> {vm.structured.calendar!r}\n"
            f"\tctx.external_start_dates -> {vm.valid_start_dates}\n"
        )
        vm.structured.errors.append(msg)
