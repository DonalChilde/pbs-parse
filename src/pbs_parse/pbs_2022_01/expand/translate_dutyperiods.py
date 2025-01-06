"""FILE: translate_dutyperiods.py."""

import logging
from collections.abc import Sequence
from datetime import datetime

import pbs_parse.pbs_2022_01.models.expanded as ET
import pbs_parse.pbs_2022_01.models.structured as ST
from pbs_parse.pbs_2022_01.expand.state import State
from pbs_parse.pbs_2022_01.expand.translate_dutyperiod import translate_dutyperiod

logger = logging.getLogger(__name__)


def translate_dutyperiods(
    first_report_utc: datetime,
    s_dutyperiods: Sequence[ST.DutyPeriod],
    state: State,
) -> tuple[list[ET.DutyPeriod], State]:
    """translate_dutyperiods.

    Args:
        first_report_utc (datetime): _description_
        s_dutyperiods (Sequence[ST.DutyPeriod]): _description_
        state (State): _description_

    Returns:
        tuple[list[ET.DutyPeriod], State]: _description_
    """
    dutyperiods: list[ET.DutyPeriod] = []
    report_utc = first_report_utc
    for idx, s_dutyperiod in enumerate(s_dutyperiods, start=1):
        state.dp_idx = idx
        logger.debug(
            "Translating dutyperiod %d with report_utc %s",
            state.dp_idx,
            report_utc.isoformat(),
        )
        try:
            next_report_lcl = s_dutyperiods[idx].report_time.lcl
        except IndexError:
            next_report_lcl = ""
        dutyperiod, state = translate_dutyperiod(
            report_utc=report_utc,
            next_report_lcl=next_report_lcl,
            s_dutyperiod=s_dutyperiod,
            state=state,
        )
        dutyperiods.append(dutyperiod)
        if dutyperiod.layover is not None:
            report_utc = dutyperiod.release_utc + dutyperiod.layover.rest
    return (dutyperiods, state)
