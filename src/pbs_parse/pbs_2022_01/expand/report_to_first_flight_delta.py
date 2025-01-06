"""FILE: report_to_first_flight_delta.py."""

import logging
from datetime import timedelta

import pbs_parse.pbs_2022_01.models.structured as ST

logger = logging.getLogger(__name__)


def report_to_first_flight_delta(s_dutyperiod: ST.DutyPeriod) -> timedelta:
    """Get the delta between report and the first flight.

    report to first departure should be 1 hour or 30 min for dh leg.
    """
    if s_dutyperiod.flights[0].deadhead:
        td_delta = timedelta(minutes=30)
    else:
        td_delta = timedelta(hours=1)
    return td_delta
