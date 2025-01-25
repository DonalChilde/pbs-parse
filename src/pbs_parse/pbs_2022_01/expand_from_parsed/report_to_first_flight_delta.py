"""FILE: report_to_first_flight_delta.py."""

import logging
from datetime import timedelta

from pbs_parse.pbs_2022_01.models.collated_trip import CollatedDutyPeriod

logger = logging.getLogger(__name__)


def report_to_first_flight_delta(collated_dp: CollatedDutyPeriod) -> timedelta:
    """Get the delta between report and the first flight.

    report to first departure should be 1 hour normally, or 30 min for dh leg.
    """
    if collated_dp.flights[0].data["deadhead"]:
        td_delta = timedelta(minutes=30)
    else:
        td_delta = timedelta(hours=1)
    return td_delta
