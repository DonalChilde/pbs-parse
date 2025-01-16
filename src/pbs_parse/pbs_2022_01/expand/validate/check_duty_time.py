"""FILE: check_duty_time.py."""

from datetime import timedelta

from pbs_parse.pbs_2022_01.models.expanded_validation import ExpandedValidation


def check_duty_time(vm: ExpandedValidation) -> None:
    """Check duty time."""
    for dp_idx, dutyperiods in enumerate(
        zip(vm.expanded.dutyperiods, vm.structured.dutyperiods, strict=True),
        start=1,
    ):
        e_dutyperiod, s_dutyperiod = dutyperiods
        e_calculated_duty_time = e_dutyperiod.release_utc - e_dutyperiod.report_utc
        if e_calculated_duty_time != e_dutyperiod.duty:
            msg = (
                f"Expanded duty time for dutyperiod {dp_idx} does not match calculated duty time. "
                f"{e_calculated_duty_time=}, {e_dutyperiod.duty=}, {e_dutyperiod.report_utc=}, {e_dutyperiod.release_utc=}"
            )
            vm.errors.append(msg)
        hours, minutes = s_dutyperiod.duty.split(".", maxsplit=1)
        s_duty_time = timedelta(hours=int(hours), minutes=int(minutes))
        if e_calculated_duty_time != s_duty_time:
            msg = (
                f"Expanded duty time for dutyperiod {dp_idx} does not match parsed duty time. "
                f"{e_calculated_duty_time=}, {s_dutyperiod.duty=}, {e_dutyperiod.report_utc=}, {e_dutyperiod.release_utc=}"
            )

            vm.errors.append(msg)
