"""Models related to pbs trips and pages."""

# ruff: noqa: D101 D102 D103
from dataclasses import dataclass, field
from typing import TypedDict
from uuid import NAMESPACE_DNS, UUID, uuid4, uuid5

from pfmsoft.indexed_string.model import IndexedString, IndexedStringTD
from pfmsoft.simple_serializer import DataclassSerializer

PAGE_LINES_NS = uuid5(NAMESPACE_DNS, "pbs_split.pbs_2022_01.page_lines")
TRIP_LINES_NS = uuid5(NAMESPACE_DNS, "pbs_split.pbs_2022_01.trip_lines")


class PageLinesTD(TypedDict):
    uuid: str
    idx: int
    lines: list[IndexedStringTD]


class TripLinesTD(TypedDict):
    uuid: str
    source: str
    idx: int
    lines: list[IndexedStringTD]


@dataclass(slots=True)
class PageLines:
    idx: int
    uuid: str = ""
    lines: list[IndexedString] = field(default_factory=list)

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
        # data = asdict(self)
        # data.pop("uuid", None)
        # return uuid5(PAGE_LINES_NS, repr(data))
        return uuid4()

    @staticmethod
    def from_simple(simple_obj: PageLinesTD) -> "PageLines":
        result = PageLines(
            uuid=simple_obj["uuid"],
            idx=simple_obj["idx"],
            lines=[IndexedString(**x) for x in simple_obj["lines"]],
        )
        return result


@dataclass(slots=True)
class TripLines:
    source: str
    idx: int
    uuid: str = ""
    lines: list[IndexedString] = field(default_factory=list)

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
        # data = asdict(self)
        # data.pop("uuid", None)
        # return uuid5(TRIP_LINES_NS, repr(data))
        return uuid4()

    @staticmethod
    def from_simple(simple_obj: TripLinesTD) -> "TripLines":
        result = TripLines(
            uuid=simple_obj["uuid"],
            source=simple_obj["source"],
            idx=simple_obj["idx"],
            lines=[IndexedString(**x) for x in simple_obj["lines"]],
        )
        return result


def page_lines_serializer() -> DataclassSerializer[PageLines, PageLinesTD]:
    return DataclassSerializer[PageLines, PageLinesTD](
        complex_factory=PageLines.from_simple
    )


def trip_lines_serializer() -> DataclassSerializer[TripLines, TripLinesTD]:
    return DataclassSerializer[TripLines, TripLinesTD](
        complex_factory=TripLines.from_simple
    )
