"""Models for Parsed trips."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict
from uuid import NAMESPACE_DNS, UUID, uuid5

from pfmsoft.simple_serializer import DataclassSerializer
from pfmsoft.state_parser import model

PARSED_TRIP_NS = uuid5(NAMESPACE_DNS, "pbs_parse.pbs_2022_01.parsed_trip")


class ParsedTripTD(TypedDict):
    """A simple object version of ParsedTrip."""

    uuid: str
    source: str
    parsed_lines: list[model.ParsedIndexedStringTD]


@dataclass(slots=True)
class ParsedTrip:
    """ParsedTrip contains the parsed lines of a pbs trip."""

    source: str
    uuid: str = ""
    parsed_lines: list[model.ParsedIndexedString] = field(default_factory=list)

    def __post_init__(self):
        """Init the uuid if missing, validate if not missing."""
        current_uuid_str = str(self.make_uuid())
        if self.uuid == "":
            self.uuid = current_uuid_str
            return
        # if self.uuid != current_uuid_str:
        #     raise ValueError(
        #         f"Supplied uuid: {self.uuid} does not match calculated uuid: {current_uuid_str}"
        #     )

    def make_uuid(self) -> UUID:
        """Make a uuid from a namespace and the repr of asdict(self), minus the uuid field."""
        return uuid5(namespace=PARSED_TRIP_NS, name=self.source)
        # # data = asdict(self)
        # # data.pop("uuid", None)
        # # return uuid5(PARSED_TRIP_NS, repr(data))
        # return uuid4()

    @staticmethod
    def from_simple(simple_obj: ParsedTripTD) -> "ParsedTrip":
        """Reconstitute a ParsedTrip from a simple object."""
        result = ParsedTrip(
            uuid=simple_obj["uuid"],
            source=simple_obj["source"],
            parsed_lines=[
                model.ParsedIndexedString.from_simple(x)
                for x in simple_obj["parsed_lines"]
            ],
        )
        return result

    def __str__(self) -> str:
        """Make a str rep of ParsedTrip."""
        lines: list[str] = []
        lines.append(f"uuid: {self.uuid}")
        lines.append(f"source: {self.source}")
        lines.append("Text Input:")
        lines.extend(f"{x.indexed_string}" for x in self.parsed_lines)
        lines.append("Parsed Data:")
        lines.extend(
            f"ID: {x.id} {x.indexed_string.idx}: {x.data!r}" for x in self.parsed_lines
        )
        return "\n".join(lines)


def parsed_trip_serializer() -> DataclassSerializer[ParsedTrip, ParsedTripTD]:
    """Construct a serializer for Parsedtrip."""
    return DataclassSerializer[ParsedTrip, ParsedTripTD](
        complex_factory=ParsedTrip.from_simple
    )


PARSED_TRIP_SERIALIZER = parsed_trip_serializer()


def default_file_name(path_name: str) -> str:
    """Make the default file name for ParsedTrip."""
    return f"{Path(path_name).stem}.parsed.json"
