from typing import Dict, Sequence

from pbs_parse.pbs_2022_01.parser import parsers
from pbs_parse.snippets.indexed_string.state_parser.protocols import (
    IndexedStringParserProtocol,
)


def parse_table() -> Dict[str, Sequence[IndexedStringParserProtocol]]:
    scheme: Dict[str, Sequence[IndexedStringParserProtocol]] = {
        "start": [
            parsers.PageHeader1(state="page_header_1"),
        ],
        "page_header_1": [
            parsers.PageHeader2(state="page_header_2"),
        ],
        "page_header_2": [
            parsers.TripHeader(state="trip_header"),
            parsers.BaseEquipment("base_equipment"),
        ],
        # "HeaderSeparator": [
        #     parsers.TripHeader(),
        #     parsers.BaseEquipment(),
        # ],
        "base_equipment": [
            parsers.TripHeader(state="trip_header"),
        ],
        "trip_header": [
            parsers.DutyPeriodReport(state="duty_period_report"),
            parsers.PriorMonthDeadhead(state="prior_month_deadhead"),
        ],
        "prior_month_deadhead": [
            parsers.DutyPeriodReport(state="duty_period_report"),
        ],
        "duty_period_report": [
            parsers.Flight(state="flight"),
            parsers.FlightDeadhead(state="flight"),
        ],
        "flight": [
            parsers.Flight(state="flight"),
            parsers.FlightDeadhead(state="flight"),
            parsers.DutyPeriodRelease(state="duty_period_release"),
        ],
        "duty_period_release": [
            parsers.Layover(state="layover"),
            parsers.TripFooter(state="trip_footer"),
        ],
        "layover": [
            parsers.DutyPeriodReport(state="duty_period_report"),
            parsers.Transportation(state="transportation"),
            parsers.HotelAdditional(state="hotel_additional"),
        ],
        "transportation": [
            parsers.DutyPeriodReport(state="duty_period_report"),
            parsers.HotelAdditional(state="hotel_additional"),
        ],
        "hotel_additional": [
            parsers.DutyPeriodReport(state="duty_period_report"),
            parsers.TransportationAdditional(state="transportation_additional"),
        ],
        "transportation_additional": [
            parsers.DutyPeriodReport(state="duty_period_report"),
            parsers.HotelAdditional(state="hotel_additional"),
        ],
        "trip_footer": [
            parsers.PageFooter(state="page_footer"),
            parsers.CalendarOnly(state="calendar_only"),
        ],
        # "CalendarOnly": [
        #     parsers.TripSeparator(state="calendar_only"),
        # ],
        # "TripSeparator": [
        #     parsers.TripHeader(state=),
        #     parsers.PageFooter(state=),
        # ],
        # "PageFooter": [
        #     parsers.PageHeader1(state=),
        # ],
    }
    return scheme
