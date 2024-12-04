"""Defines the parser lookup table."""

from collections.abc import Sequence

from pfmsoft.state_parser.abc import ParserABC

from pbs_parse.pbs_2022_01.parse import grammar_2 as G
from pbs_parse.pbs_2022_01.parse.parsers_2 import PageHeader1
from pbs_parse.pbs_2022_01.parse.parsers_2 import SimplePyparsingParser as SPP


def parse_table() -> dict[str, Sequence[ParserABC]]:
    """Define the parer lookup table."""
    scheme: dict[str, Sequence[ParserABC]] = {
        "start": [
            PageHeader1(state="page_header_1"),
        ],
        "page_header_1": [
            SPP(state="page_header_2", string_parser=G.page_header_2),
        ],
        "page_header_2": [
            SPP(state="trip_header", string_parser=G.trip_header),
            SPP(state="base_equipment", string_parser=G.base_equipment),
        ],
        "base_equipment": [
            SPP(state="trip_header", string_parser=G.trip_header),
        ],
        "trip_header": [
            SPP(state="duty_period_report", string_parser=G.dutyperiod_report),
            # SPP(state="prior_month_deadhead",),
        ],
        "prior_month_deadhead": [
            SPP(state="duty_period_report", string_parser=G.dutyperiod_report),
        ],
        "duty_period_report": [
            SPP(state="flight", string_parser=G.flight),
            SPP(state="flight", string_parser=G.flight_deadhead),
        ],
        "flight": [
            SPP(state="flight", string_parser=G.flight),
            SPP(state="flight", string_parser=G.flight_deadhead),
            SPP(state="duty_period_release", string_parser=G.dutyperiod_release),
        ],
        "duty_period_release": [
            SPP(state="layover", string_parser=G.layover),
            SPP(state="trip_footer", string_parser=G.trip_footer),
        ],
        "layover": [
            SPP(state="duty_period_report", string_parser=G.dutyperiod_report),
            SPP(state="transportation", string_parser=G.transportation),
            SPP(state="hotel_additional", string_parser=G.hotel_additional),
        ],
        "transportation": [
            SPP(state="duty_period_report", string_parser=G.dutyperiod_report),
            SPP(state="hotel_additional", string_parser=G.hotel_additional),
        ],
        "hotel_additional": [
            SPP(state="duty_period_report", string_parser=G.dutyperiod_report),
            SPP(state="transportation_additional", string_parser=G.transportation),
        ],
        "transportation_additional": [
            SPP(state="duty_period_report", string_parser=G.dutyperiod_report),
            SPP(state="hotel_additional", string_parser=G.hotel_additional),
        ],
        "trip_footer": [
            SPP(state="page_footer", string_parser=G.page_footer),
            SPP(state="calendar_only", string_parser=G.calendar_only),
        ],
        "calendar_only": [
            SPP(state="page_footer", string_parser=G.calendar_only),
        ],
    }
    return scheme
