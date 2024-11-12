import logging
import re
from typing import Any

import pyparsing as pp

from pbs_parse.pbs_2022_01.parser import grammar
from pbs_parse.snippets.indexed_string.protocols import IndexedStringProtocol
from pbs_parse.snippets.indexed_string.state_parser.model import (
    ParsedIndexedString,
    ParseResult,
)
from pbs_parse.snippets.indexed_string.state_parser.parse_exception import (
    SingleParserFail,
)
from pbs_parse.snippets.indexed_string.state_parser.parsers import ParserABC
from pbs_parse.snippets.indexed_string.state_parser.protocols import (
    ParseContextProtocol,
    ParseResultProtocol,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PyparsingParser(ParserABC):
    def __init__(self, state: str) -> None:
        super().__init__(state)

    p_parser: pp.ParserElement

    def get_result(self, indexed_string: IndexedStringProtocol) -> dict[str, Any]:
        try:
            result = self.p_parser.parse_string(indexed_string.txt)
            result_dict: dict[str, Any] = result.as_dict()  # type: ignore
        except pp.ParseException as error:
            raise SingleParserFail(
                f"{error}",
                parser=self,
                indexed_string=indexed_string,
            ) from error
        return result_dict

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        raise NotImplementedError


class PageHeader1(ParserABC):
    def __init__(self, state: str) -> None:
        super().__init__(state)

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        if "DEPARTURE" in input.txt:
            result = ParsedIndexedString(id=self.state, indexed_string=input, data={})
            return ParseResult(current_state=self.state, result=result)

        raise SingleParserFail(
            f"'DEPARTURE' not found in {input!r}.",
            parser=self,
            indexed_string=input,
        )


class PageHeader2(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.PageHeader2

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.PageHeader2(
        #     from_date="".join(result_dict.get("from_date", "")),
        #     to_date="".join(result_dict.get("to_date", "")),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


class HeaderSeparator(ParserABC):
    def __init__(self, state: str) -> None:
        super().__init__(state)

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        if "-" * 5 in input.txt or "\u2212" * 5 in input.txt:
            # parsed_data = models.HeaderSeparator()
            result = ParsedIndexedString(id=self.state, indexed_string=input, data={})
            return ParseResult(current_state=self.state, result=result)
        raise SingleParserFail(
            "'-----' not found in line.",
            parser=self,
            indexed_string=input,
        )


class TripSeparator(ParserABC):
    def __init__(self, state: str) -> None:
        super().__init__(state)

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        if "-" * 5 in input.txt or "\u2212" * 5 in input.txt:
            # parsed_data = models.TripSeparator()
            # result = ParsedIndexedString(
            #     id=self.state, indexed_string=input, data=result_dict
            # )
            result = ParsedIndexedString(id=self.state, indexed_string=input, data={})
            return ParseResult(current_state=self.state, result=result)
        raise SingleParserFail(
            "'-----' not found in line.",
            parser=self,
            indexed_string=input,
        )


class BaseEquipment(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.BaseEquipment

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)

        # parsed_data = models.BaseEquipment(
        #     base=result_dict.get("base", ""),
        #     satellite_base=result_dict.get("satelite_base", ""),
        #     equipment=result_dict.get("equipment", ""),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


class TripHeader(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        # FIXME build progressive match, with options,
        # loop over list of possibles, take first match
        self.p_parser = grammar.TripHeader

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.TripHeader(
        #     number=result_dict.get("number", ""),
        #     ops_count=result_dict.get("ops_count", ""),
        #     positions=" ".join(result_dict.get("positions", "")),
        #     operations=" ".join(result_dict.get("operations", "")),
        #     qualifications=" ".join(result_dict.get("qualifications", "")),
        #     # calendar="",
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


# TODO is this parser neeed?
class PriorMonthDeadhead(ParserABC):
    def __init__(self, state: str) -> None:
        super().__init__(state)

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        if "PRIOR" in input.txt:
            # parsed_data = models.PriorMonthDeadhead()
            result = ParsedIndexedString(id=self.state, indexed_string=input, data={})
            return ParseResult(current_state=self.state, result=result)
        raise SingleParserFail(
            "'PRIOR' not found in line.",
            parser=self,
            indexed_string=input,
        )


class DutyPeriodReport(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.DutyPeriodReport

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.DutyPeriodReport(
        #     report=result_dict.get("report", ""),
        #     calendar=result_dict.get("calendar_entries", []),
        # )
        # parsed_data.calendar.extend(result_dict.get("calendar_entries", []))
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


# 4  4/4 64 2578D MIA 1949/1649    SAN 2220/2220    AA    5.31
# 2  2/2 45 1614D MCI 1607/1407    DFW 1800/1600    AA    1.53   1.27X


class Flight(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.Flight

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.Flight(
        #     dutyperiod_idx=result_dict.get("dutyperiod", ""),
        #     dep_arr_day=result_dict.get("day_of_sequence", ""),
        #     eq_code=result_dict.get("equipment_code", ""),
        #     flight_number=result_dict.get("flight_number", ""),
        #     deadhead="",
        #     departure_station=result_dict.get("departure_station", ""),
        #     departure_time=result_dict.get("departure_time", ""),
        #     meal=result_dict.get("crew_meal", ""),
        #     arrival_station=result_dict.get("arrival_station", ""),
        #     arrival_time=result_dict.get("arrival_time", ""),
        #     block=result_dict.get("block", ""),
        #     synth="0.00",
        #     ground=result_dict.get("ground", ""),
        #     equipment_change=result_dict.get("equipment_change", ""),
        #     calendar=result_dict.get("calendar_entries", []),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


# 4  4/4 64 2578D MIA 1949/1649    SAN 2220/2220    AA    5.31
# 2  2/2 45 1614D MCI 1607/1407    DFW 1800/1600    AA    1.53   1.27X
class FlightDeadhead(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.FlightDeadhead

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.Flight(
        #     dutyperiod_idx=result_dict.get("dutyperiod", ""),
        #     dep_arr_day=result_dict.get("day_of_sequence", ""),
        #     eq_code=result_dict.get("equipment_code", ""),
        #     flight_number=result_dict.get("flight_number", ""),
        #     deadhead=result_dict.get("deadhead", ""),
        #     departure_station=result_dict.get("departure_station", ""),
        #     departure_time=result_dict.get("departure_time", ""),
        #     meal=result_dict.get("crew_meal", ""),
        #     arrival_station=result_dict.get("arrival_station", ""),
        #     arrival_time=result_dict.get("arrival_time", ""),
        #     block="0.00",
        #     synth=result_dict.get("synth", ""),
        #     ground=result_dict.get("ground", ""),
        #     equipment_change=result_dict.get("equipment_change", ""),
        #     calendar=result_dict.get("calendar_entries", []),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


class DutyPeriodRelease(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.DutyPeriodRelease

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.DutyPeriodRelease(
        #     release=result_dict.get("release_time", ""),
        #     block=result_dict.get("block", ""),
        #     synth=result_dict.get("synth", ""),
        #     total_pay=result_dict.get("total_pay", ""),
        #     duty=result_dict.get("duty", ""),
        #     flight_duty=result_dict.get("flight_duty", ""),
        #     calendar=result_dict.get("calendar_entries", []),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


class Layover(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.Layover

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.Layover(
        #     layover_city=result_dict.get("layover_city", ""),
        #     name=result_dict.get("hotel", ""),
        #     phone=result_dict.get("hotel_phone", ""),
        #     rest=result_dict.get("rest", ""),
        #     calendar=result_dict.get("calendar_entries", []),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


class HotelAdditional(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.HotelAdditional

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.HotelAdditional(
        #     layover_city=result_dict.get("layover_city", ""),
        #     name=result_dict.get("hotel", ""),
        #     phone=result_dict.get("hotel_phone", ""),
        #     calendar=result_dict.get("calendar_entries", []),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


class Transportation(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.Transportation

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.Transportation(
        #     name=result_dict.get("transportation", ""),
        #     phone=result_dict.get("phone", ""),
        #     calendar=result_dict.get("calendar_entries", []),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


class TransportationAdditional(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.TransportationAdditional

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx

        result_dict = self.get_result(indexed_string=input)
        # try:
        #     parsed_data = models.TransportationAdditional(
        #         name=result_dict.get("transportation", ""),
        #         phone=result_dict.get("transportation_phone", ""),
        #         calendar=result_dict.get("calendar_entries", []),
        #     )
        # except KeyError as error:
        #     raise SingleParserFail(
        #         f"Key missing in parsed_data {indexed_string!r}. Is there no transportation name? {str(error)}",
        #         parser=self,
        #         indexed_string=input,
        #     ) from error
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


class TripFooter(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.TripFooter

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.TripFooter(
        #     block=result_dict.get("block", ""),
        #     synth=result_dict.get("synth", ""),
        #     total_pay=result_dict.get("total_pay", ""),
        #     tafb=result_dict.get("tafb", ""),
        #     calendar=result_dict.get("calendar_entries", []),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


class CalendarOnly(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.CalendarOnly

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        expected_len = 20
        ws_len = len(get_leading_whitespace(input.txt))
        if ws_len < expected_len:
            raise SingleParserFail(
                f"Expected at least {expected_len} leading whitespace characters, got {ws_len}",
                parser=self,
                indexed_string=input,
            )
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.CalendarOnly(
        #     calendar=result_dict.get("calendar_entries", []),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)


def get_leading_whitespace(txt: str) -> str:
    # TODO move to snippet
    # https://stackoverflow.com/a/2268559/105844
    matched = re.match(r"\s*", txt)
    if matched is None:
        return ""
    return matched.group()


class PageFooter(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.PageFooter

    def parse(
        self, ctx: ParseContextProtocol, input: IndexedStringProtocol
    ) -> ParseResultProtocol:
        _ = ctx
        result_dict = self.get_result(indexed_string=input)
        # parsed_data = models.PageFooter(
        #     issued=result_dict.get("issued", ""),
        #     effective=result_dict.get("effective", ""),
        #     base=result_dict.get("base", ""),
        #     satelite_base=result_dict.get("satelite_base", ""),
        #     equipment=result_dict.get("equipment", ""),
        #     division=result_dict.get("division", ""),
        #     page=result_dict.get("internal_page", ""),
        # )
        result = ParsedIndexedString(
            id=self.state, indexed_string=input, data=result_dict
        )
        return ParseResult(current_state=self.state, result=result)
