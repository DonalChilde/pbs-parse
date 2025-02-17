"""Defines the parser lookup table."""

from collections.abc import Sequence

from pbs_parse.pbs_2022_01.parse import grammar as G
from pbs_parse.pbs_2022_01.parse.parsers import PageHeader1
from pbs_parse.pbs_2022_01.parse.parsers import SimplePyparsingParser as SPP
from pbs_parse.snippets.indexed_string_state_parser import protocol as P


def parse_table() -> dict[str, Sequence[P.Parser]]:
    """Define the parer lookup table."""
    scheme: dict[str, Sequence[P.Parser]] = {
        "start": [
            PageHeader1(state="page_header_1"),
        ],
        "page_header_1": [
            SPP(parsed_state="page_header_2", string_parser=G.page_header_2),
        ],
        "page_header_2": [
            SPP(parsed_state="trip_header", string_parser=G.trip_header),
            SPP(parsed_state="base_equipment", string_parser=G.base_equipment),
        ],
        "base_equipment": [
            SPP(parsed_state="trip_header", string_parser=G.trip_header),
        ],
        "trip_header": [
            SPP(parsed_state="duty_period_report", string_parser=G.dutyperiod_report),
            # SPP(state="prior_month_deadhead",)
        ],
        "prior_month_deadhead": [
            SPP(parsed_state="duty_period_report", string_parser=G.dutyperiod_report),
        ],
        "duty_period_report": [
            SPP(parsed_state="flight", string_parser=G.flight),
            SPP(parsed_state="flight", string_parser=G.flight_deadhead),
        ],
        "flight": [
            SPP(parsed_state="flight", string_parser=G.flight),
            SPP(parsed_state="flight", string_parser=G.flight_deadhead),
            SPP(parsed_state="duty_period_release", string_parser=G.dutyperiod_release),
        ],
        "duty_period_release": [
            SPP(parsed_state="layover", string_parser=G.layover),
            SPP(parsed_state="trip_footer", string_parser=G.trip_footer),
        ],
        "layover": [
            SPP(parsed_state="duty_period_report", string_parser=G.dutyperiod_report),
            SPP(parsed_state="transportation", string_parser=G.transportation),
            SPP(parsed_state="hotel_additional", string_parser=G.hotel_additional),
        ],
        "transportation": [
            SPP(parsed_state="duty_period_report", string_parser=G.dutyperiod_report),
            SPP(parsed_state="hotel_additional", string_parser=G.hotel_additional),
        ],
        "hotel_additional": [
            SPP(parsed_state="duty_period_report", string_parser=G.dutyperiod_report),
            SPP(
                parsed_state="transportation_additional", string_parser=G.transportation
            ),
        ],
        "transportation_additional": [
            SPP(parsed_state="duty_period_report", string_parser=G.dutyperiod_report),
            SPP(parsed_state="hotel_additional", string_parser=G.hotel_additional),
        ],
        "trip_footer": [
            SPP(parsed_state="page_footer", string_parser=G.page_footer),
            SPP(parsed_state="calendar_only", string_parser=G.calendar_only),
        ],
        "calendar_only": [
            SPP(parsed_state="page_footer", string_parser=G.page_footer),
        ],
    }
    return scheme
