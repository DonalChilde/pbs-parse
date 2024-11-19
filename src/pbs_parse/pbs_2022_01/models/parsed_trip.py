from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict

from pfmsoft.simple_serializer import DataclassSerializer
from pfmsoft.state_parser import model


class ParsedTripTD(TypedDict):
    uuid: str
    source: str
    parsed_lines: list[model.ParsedIndexedStringTD]


@dataclass(slots=True)
class ParsedTrip:
    uuid: str
    source: str
    parsed_lines: list[model.ParsedIndexedString] = field(default_factory=list)

    @staticmethod
    def from_simple(simple_obj: ParsedTripTD) -> "ParsedTrip":
        result = ParsedTrip(
            uuid=simple_obj["uuid"],
            source=simple_obj["source"],
            parsed_lines=[
                model.ParsedIndexedString.from_simple(x)
                for x in simple_obj["parsed_lines"]
            ],
        )
        return result


def parsed_trip_serializer() -> DataclassSerializer[ParsedTrip, ParsedTripTD]:
    return DataclassSerializer[ParsedTrip, ParsedTripTD](
        complex_factory=ParsedTrip.from_simple
    )


def default_file_name(path_name: str) -> str:
    return f"{Path(path_name).stem}.parsed.json"
