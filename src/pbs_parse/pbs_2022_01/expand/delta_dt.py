"""FILE: delta_dt.py."""

import logging
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from pbs_parse.pbs_2022_01.expand.next_local_time_in_utc import next_local_time_in_utc
from pbs_parse.pbs_2022_01.expand.state import State

logger = logging.getLogger(__name__)


def delta_dt(
    utc_ref: datetime,
    td: timedelta,
    lcl_ref: str,
    lcl_tz: str,
    field_name: str,
    state: State,
) -> tuple[datetime, State]:
    """Get next utc time from uncertain info.

    Pbs pairing packages have some incorrect info sometimes.
    - during the nov. fold, a layover rest duration was an hour short when compared to release/report.

    figure out whether to use td addition, or next time calc to get accurate next utc.

    Args:
        utc_ref (datetime): _description_
        td (timedelta): _description_
        lcl_ref (str): _description_
        lcl_tz (str): _description_
        field_name (str): foo
        state (State): foo

    Returns:
        datetime: _description_
    """
    lcl_tzinfo = ZoneInfo(lcl_tz)

    dt_utc_addition = utc_ref + td
    # dt_lcl_addition = dt_utc_addition.astimezone(lcl_tzinfo)
    return (dt_utc_addition, state)
    # if dt_lcl_addition.strftime("%H%M") == lcl_ref:
    #     return (dt_utc_addition, state)
    # utc_ref_lcl = utc_ref.astimezone(lcl_tzinfo)
    # dt_utc_next = next_local_time_in_utc(
    #     utc_start=utc_ref,
    #     next_lcl=time.fromisoformat(lcl_ref),
    #     next_tz_name=lcl_tz,
    # )
    # dt_lcl_next = dt_utc_next.astimezone(lcl_tzinfo)

    # logger.info(
    #     "for dp: %d flt %d field: %s Delta addition did not match lcl_ref. ",
    #     state.dp_idx,
    #     state.flight_idx,
    #     field_name,
    # )
    # logger.info(
    #     "Inputs: utc_ref: %s, td: %s, lcl_ref: %s, lcl_tz: %s, utc_ref_lcl: %s ",
    #     utc_ref.isoformat(),
    #     td,
    #     lcl_ref,
    #     lcl_tz,
    #     utc_ref_lcl.isoformat(),
    # )
    # logger.info(
    #     "Addition: %s %s ", dt_utc_addition.isoformat(), dt_lcl_addition.isoformat()
    # )
    # logger.info(
    #     "Trying `next_local_time_in_utc`. %s %s",
    #     dt_utc_next.isoformat(),
    #     dt_lcl_next.isoformat(),
    # )
    return (dt_utc_next, state)
