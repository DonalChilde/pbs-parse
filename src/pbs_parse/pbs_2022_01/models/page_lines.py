"""pages lines."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict
from uuid import NAMESPACE_DNS, UUID, uuid5

from pfmsoft.indexed_string.index_strings import make_uuid_iter
from pfmsoft.indexed_string.model import IndexedString, IndexedStringTD
from pfmsoft.simple_serializer import DataclassSerializer

from pbs_parse.snippets.file.data_file_loader import DataFileLoader

PAGE_LINES_NS = uuid5(NAMESPACE_DNS, "pbs_split.pbs_2022_01.page_lines")


class PageLinesTD(TypedDict):
    """PageLinesTD."""

    uuid: str
    idx: str
    lines: list[IndexedStringTD]


@dataclass(slots=True)
class PageLines:
    """PageLines."""

    idx: str
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
        return self.assemble_file_name(idx=self.idx, uuid=self.uuid)

    @staticmethod
    def assemble_file_name(idx: str, uuid: str) -> str:
        """assemble_file_name.

        Args:
            idx (str): _description_
            uuid (str): _description_

        Returns:
            str: _description_
        """
        return f"page-lines_{idx}_{uuid}.json"


def page_lines_serializer() -> DataclassSerializer[PageLines, PageLinesTD]:
    """page_lines_serializer.

    Returns:
        DataclassSerializer[PageLines, PageLinesTD]: _description_
    """
    return DataclassSerializer[PageLines, PageLinesTD](
        complex_factory=PageLines.from_simple
    )


PAGE_LINES_SERIALIZER = page_lines_serializer()


class PageLinesSaver:
    """PageLinesSaver."""

    def __init__(self, path_out: Path) -> None:
        """Save PageLines to a directory using the default file name.

        Args:
            path_out (Path): The directory to save the PageLines to.
        """
        if path_out.is_file():
            raise ValueError(
                f"Path out is an existing file, should be a directory. {path_out=}"
            )
        self.path_out = path_out

    def __call__(self, page_lines: PageLines, overwrite: bool = False) -> Path:
        """Save PageLines to a directory using the default file name.

        Args:
            page_lines (PageLines): The PageLines to save.
            overwrite (bool): Overwrite existing files.

        Returns:
            Path: The path to the saved file.
        """
        path_out = self.path_out / page_lines.default_file_name()
        PAGE_LINES_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=page_lines, overwrite=overwrite
        )
        return path_out


class PageLinesLoader(DataFileLoader[PageLines]):
    """PageLinesLoader."""

    def __init__(self, path_in: Path, glob: str = "page-lines_*.json") -> None:
        """Load PageLines from directory.

        Args:
            path_in (Path): The directory to load files from.
            glob (str, optional): The glob to match files. Defaults to "page-lines_*.json".
        """
        super().__init__(path_in, glob)

    def _translate(self, obj_path: Path) -> PageLines:
        return PAGE_LINES_SERIALIZER.load_from_json(path_in=obj_path)
