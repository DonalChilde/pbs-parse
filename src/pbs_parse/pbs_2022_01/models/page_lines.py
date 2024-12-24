"""pages lines."""

from dataclasses import dataclass, field
from typing import TypedDict
from uuid import NAMESPACE_DNS, UUID, uuid5

from pfmsoft.indexed_string.index_strings import make_uuid_iter
from pfmsoft.indexed_string.model import IndexedString, IndexedStringTD
from pfmsoft.simple_serializer import DataclassSerializer

PAGE_LINES_NS = uuid5(NAMESPACE_DNS, "pbs_split.pbs_2022_01.page_lines")


class PageLinesTD(TypedDict):
    """PageLinesTD."""

    uuid: str
    idx: int
    lines: list[IndexedStringTD]


@dataclass(slots=True)
class PageLines:
    """PageLines."""

    idx: int
    uuid: str = ""
    lines: list[IndexedString] = field(default_factory=list)

    def __post_init__(self):
        """Init the uuid if missing, validate if not missing."""
        current_uuid_str = str(self.make_uuid())
        if self.uuid == "":
            self.uuid = current_uuid_str
            return
        if self.uuid != current_uuid_str:
            raise ValueError(
                f"Supplied uuid: {self.uuid} does not match calculated uuid: {current_uuid_str}"
            )

    def make_uuid(self) -> UUID:
        """Make a uuid from a namespace and the lines."""
        return make_uuid_iter(indexed_strings=self.lines, namespace=PAGE_LINES_NS)

    @staticmethod
    def from_simple(simple_obj: PageLinesTD) -> "PageLines":
        """from_simple.

        Args:
            simple_obj (PageLinesTD): _description_

        Returns:
            PageLines: _description_
        """
        result = PageLines(
            uuid=simple_obj["uuid"],
            idx=simple_obj["idx"],
            lines=[IndexedString(**x) for x in simple_obj["lines"]],
        )
        return result

    def default_file_name(self) -> str:
        """default_file_name.

        Returns:
            str: _description_
        """
        return f"page-lines_{self.idx}_{self.uuid}.json"


def page_lines_serializer() -> DataclassSerializer[PageLines, PageLinesTD]:
    """page_lines_serializer.

    Returns:
        DataclassSerializer[PageLines, PageLinesTD]: _description_
    """
    return DataclassSerializer[PageLines, PageLinesTD](
        complex_factory=PageLines.from_simple
    )


PAGE_LINES_SERIALIZER = page_lines_serializer()
