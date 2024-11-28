import logging
import re
from typing import Any

import pyparsing as pp
from pfmsoft.indexed_string.model import IndexedString
from pfmsoft.state_parser.abc import ParseContextABC, ParserABC
from pfmsoft.state_parser.model import ParsedIndexedString, ParseResult
from pfmsoft.state_parser.parse_exception import SingleParserFail

from pbs_parse.pbs_2022_01.models import parsed_lines_TD as TD
from pbs_parse.pbs_2022_01.parse import grammar

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PyparsingParser(ParserABC):
    def __init__(self, state: str) -> None:
        super().__init__(state)

    p_parser: pp.ParserElement

    def get_parsed_data(self, indexed_string: IndexedString) -> dict[str, Any]:
        try:
            result = self.p_parser.parse_string(indexed_string.txt)
            parsed_data: dict[str, Any] = result.as_dict()  # type: ignore
        except pp.ParseException as error:
            raise SingleParserFail(
                f"{error}",
                parser_name=self.__class__.__name__,
                indexed_string=indexed_string,
            ) from error
        return parsed_data

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        raise NotImplementedError


class PageHeader1(ParserABC):
    def __init__(self, state: str) -> None:
        super().__init__(state)

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        if "DEPARTURE" in input.txt:
            result = ParsedIndexedString(id=self.state, indexed_string=input, data={})
            return ParseResult(current_state=self.state, parsed_indexed_string=result)

        raise SingleParserFail(
            f"'DEPARTURE' not found in {input!r}.",
            parser_name=self.__class__.__name__,
            indexed_string=input,
        )


class PageHeader2(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.PageHeader2

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.PageHeader2(
            from_date="".join(parsed_data.get("from_date", "")),
            to_date="".join(parsed_data.get("to_date", "")),
            # from_date=parsed_data.get("from_date", ""),
            # to_date=parsed_data.get("to_date", ""),
        )
        return data  # type: ignore


class HeaderSeparator(ParserABC):
    def __init__(self, state: str) -> None:
        super().__init__(state)

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        if "-" * 5 in input.txt or "\u2212" * 5 in input.txt:
            # parsed_data = models.HeaderSeparator()
            result = ParsedIndexedString(id=self.state, indexed_string=input, data={})
            return ParseResult(current_state=self.state, parsed_indexed_string=result)
        raise SingleParserFail(
            "'-----' not found in line.",
            parser_name=self.__class__.__name__,
            indexed_string=input,
        )


class TripSeparator(ParserABC):
    def __init__(self, state: str) -> None:
        super().__init__(state)

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        if "-" * 5 in input.txt or "\u2212" * 5 in input.txt:
            # parsed_data = models.TripSeparator()
            # result = ParsedIndexedString(
            #     id=self.state, indexed_string=input, data=result_dict
            # )
            result = ParsedIndexedString(id=self.state, indexed_string=input, data={})
            return ParseResult(current_state=self.state, parsed_indexed_string=result)
        raise SingleParserFail(
            "'-----' not found in line.",
            parser_name=self.__class__.__name__,
            indexed_string=input,
        )


class BaseEquipment(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.BaseEquipment

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.BaseEquipment(
            base=parsed_data.get("base", ""),
            satellite_base=parsed_data.get("satellite_base", ""),
            equipment=parsed_data.get("equipment", ""),
        )
        return data  # type: ignore


class TripHeader(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        # FIXME build progressive match, with options,
        # loop over list of possibles, take first match
        self.p_parser = grammar.TripHeader

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.TripHeader(
            number=parsed_data.get("number", ""),
            ops_count=parsed_data.get("ops_count", ""),
            positions=parsed_data.get("positions", []),
            operations=parsed_data.get("operations", []),
            qualifications=parsed_data.get("qualifications", []),
            # calendar="",
        )
        return data  # type: ignore


# TODO is this parser neeed?
class PriorMonthDeadhead(ParserABC):
    def __init__(self, state: str) -> None:
        super().__init__(state)

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        if "PRIOR" in input.txt:
            # parsed_data = models.PriorMonthDeadhead()
            result = ParsedIndexedString(id=self.state, indexed_string=input, data={})
            return ParseResult(current_state=self.state, parsed_indexed_string=result)
        raise SingleParserFail(
            "'PRIOR' not found in line.",
            parser_name=self.__class__.__name__,
            indexed_string=input,
        )


class DutyPeriodReport(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.DutyPeriodReport

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.DutyPeriodReport(
            report=parsed_data.get("report", ""),
            calendar=parsed_data.get("calendar_entries", []),
        )
        return data  # type: ignore


# 4  4/4 64 2578D MIA 1949/1649    SAN 2220/2220    AA    5.31
# 2  2/2 45 1614D MCI 1607/1407    DFW 1800/1600    AA    1.53   1.27X


class Flight(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.Flight

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.Flight(
            dutyperiod_idx=parsed_data.get("dutyperiod", ""),
            dep_arr_day=parsed_data.get("day_of_sequence", ""),
            eq_code=parsed_data.get("equipment_code", ""),
            flight_number=parsed_data.get("flight_number", ""),
            deadhead="",
            deadhead_code="",
            departure_station=parsed_data.get("departure_station", ""),
            departure_time=parsed_data.get("departure_time", ""),
            crew_meal=parsed_data.get("crew_meal", ""),
            arrival_station=parsed_data.get("arrival_station", ""),
            arrival_time=parsed_data.get("arrival_time", ""),
            block=parsed_data.get("block", ""),
            synth=parsed_data.get("synth", ""),
            ground=parsed_data.get("ground", ""),
            equipment_change=parsed_data.get("equipment_change", ""),
            calendar=parsed_data.get("calendar_entries", []),
        )
        return data  # type: ignore


# 4  4/4 64 2578D MIA 1949/1649    SAN 2220/2220    AA    5.31
# 2  2/2 45 1614D MCI 1607/1407    DFW 1800/1600    AA    1.53   1.27X
class FlightDeadhead(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.FlightDeadhead

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.Flight(
            dutyperiod_idx=parsed_data.get("dutyperiod", ""),
            dep_arr_day=parsed_data.get("day_of_sequence", ""),
            eq_code=parsed_data.get("equipment_code", ""),
            flight_number=parsed_data.get("flight_number", ""),
            deadhead=parsed_data.get("deadhead", ""),
            deadhead_code=parsed_data.get("deadhead_code", ""),
            departure_station=parsed_data.get("departure_station", ""),
            departure_time=parsed_data.get("departure_time", ""),
            crew_meal=parsed_data.get("crew_meal", ""),
            arrival_station=parsed_data.get("arrival_station", ""),
            arrival_time=parsed_data.get("arrival_time", ""),
            block="0.00",
            synth=parsed_data.get("synth", ""),
            ground=parsed_data.get("ground", ""),
            equipment_change=parsed_data.get("equipment_change", ""),
            calendar=parsed_data.get("calendar_entries", []),
        )
        return data  # type: ignore


class DutyPeriodRelease(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.DutyPeriodRelease

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.DutyPeriodRelease(
            release=parsed_data.get("release_time", ""),
            block=parsed_data.get("block", ""),
            synth=parsed_data.get("synth", ""),
            total_pay=parsed_data.get("total_pay", ""),
            duty=parsed_data.get("duty", ""),
            flight_duty=parsed_data.get("flight_duty", ""),
            calendar=parsed_data.get("calendar_entries", []),
        )
        return data  # type: ignore


class Layover(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.Layover

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.Layover(
            layover_city=parsed_data.get("layover_city", ""),
            name=parsed_data.get("hotel", ""),
            phone=parsed_data.get("hotel_phone", ""),
            rest=parsed_data.get("rest", ""),
            calendar=parsed_data.get("calendar_entries", []),
        )
        return data  # type: ignore


class HotelAdditional(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.HotelAdditional

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.HotelAdditional(
            layover_city=parsed_data.get("layover_city", ""),
            name=parsed_data.get("hotel", ""),
            phone=parsed_data.get("hotel_phone", ""),
            calendar=parsed_data.get("calendar_entries", []),
        )
        return data  # type: ignore


class Transportation(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.Transportation

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.Transportation(
            name=parsed_data.get("transportation", ""),
            phone=parsed_data.get("phone", ""),
            calendar=parsed_data.get("calendar_entries", []),
        )
        return data  # type: ignore


class TransportationAdditional(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.TransportationAdditional

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx

        result_dict = self.get_parsed_data(indexed_string=input)
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
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.TransportationAdditional(
            name=parsed_data.get("transportation", ""),
            phone=parsed_data.get("phone", ""),
            calendar=parsed_data.get("calendar_entries", []),
        )
        return data  # type: ignore


class TripFooter(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.TripFooter

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.TripFooter(
            block=parsed_data.get("block", ""),
            synth=parsed_data.get("synth", ""),
            total_pay=parsed_data.get("total_pay", ""),
            tafb=parsed_data.get("tafb", ""),
            calendar=parsed_data.get("calendar_entries", []),
        )
        return data  # type: ignore


class CalendarOnly(PyparsingParser):
    def __init__(self, state: str) -> None:
        super().__init__(state)
        self.p_parser = grammar.CalendarOnly

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        expected_len = 20
        ws_len = len(get_leading_whitespace(input.txt))
        if ws_len < expected_len:
            raise SingleParserFail(
                f"Expected at least {expected_len} leading whitespace characters, got {ws_len}",
                parser_name=self.__class__.__name__,
                indexed_string=input,
            )
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.CalendarOnly(
            calendar=parsed_data.get("calendar_entries", []),
        )
        return data  # type: ignore


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

    def parse(self, ctx: ParseContextABC, input: IndexedString) -> ParseResult:
        _ = ctx
        result_dict = self.get_parsed_data(indexed_string=input)
        data = self.translate_result(parsed_data=result_dict)
        result = ParsedIndexedString(id=self.state, indexed_string=input, data=data)
        return ParseResult(current_state=self.state, parsed_indexed_string=result)

    def translate_result(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        data = TD.PageFooter(
            issued=parsed_data.get("issued", ""),
            effective=parsed_data.get("effective", ""),
            base=parsed_data.get("base", ""),
            satellite_base=parsed_data.get("satellite_base", ""),
            equipment=parsed_data.get("equipment", ""),
            division=parsed_data.get("division", ""),
            page=parsed_data.get("internal_page", ""),
        )
        return data  # type: ignore
