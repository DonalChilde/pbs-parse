"""FILE: check_duty_time.py."""

from pbs_parse.common.parse_duration import parse_duration
from pbs_parse.pbs_2022_01.models.collated_trip import CollatedTrip
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip


def check_duty_time(expanded: ExpandedTrip, collated: CollatedTrip) -> None:
    """Check duty time."""
    for dp_idx, dutyperiods in enumerate(
        zip(expanded.dutyperiods, collated.dutyperiods, strict=True),
        start=1,
    ):
        expanded_dp, collated_dp = dutyperiods
        e_calculated_duty_time = expanded_dp.release_utc - expanded_dp.report_utc
        if e_calculated_duty_time != expanded_dp.duty:
            msg = (
                f"Expanded duty time for dutyperiod {dp_idx} does not match calculated duty time. "
                f"{e_calculated_duty_time=}, {expanded_dp.duty=}, {expanded_dp.report_utc=}, {expanded_dp.release_utc=}"
            )
            expanded.errors.append(msg)
        collated_duty = parse_duration(collated_dp.release.data["duty"])
        if e_calculated_duty_time != collated_duty:
            msg = (
                f"Expanded duty time for dutyperiod {dp_idx} does not match parsed duty time. "
                f"{e_calculated_duty_time=}, {collated_duty=}, {expanded_dp.report_utc=}, {expanded_dp.release_utc=}"
            )

            expanded.errors.append(msg)
