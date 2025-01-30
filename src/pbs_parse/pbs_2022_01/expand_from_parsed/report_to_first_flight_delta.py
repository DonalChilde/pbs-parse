"""FILE: report_to_first_flight_delta.py."""

import logging

from whenever import TimeDelta

from pbs_parse.pbs_2022_01.models.collated_trip import CollatedDutyPeriod

logger = logging.getLogger(__name__)


def report_to_first_flight_delta(collated_dp: CollatedDutyPeriod) -> TimeDelta:
    """Get the delta between report and the first flight.

    report to first departure should be 1 hour normally, or 30 min for dh leg.
    """
    if collated_dp.flights[0].data["deadhead"]:
        td_delta = TimeDelta(minutes=30)
    else:
        td_delta = TimeDelta(hours=1)
    return td_delta
