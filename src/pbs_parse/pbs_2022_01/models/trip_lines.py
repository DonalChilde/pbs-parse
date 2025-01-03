"""trip lines.."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict
from uuid import NAMESPACE_DNS, UUID, uuid5

from pfmsoft.indexed_string.index_strings import make_uuid_iter
from pfmsoft.indexed_string.model import IndexedString, IndexedStringTD
from pfmsoft.simple_serializer import DataclassSerializer

from pbs_parse.snippets.file.data_file_loader import DataFileLoader

TRIP_LINES_NS = uuid5(NAMESPACE_DNS, "pbs_split.pbs_2022_01.trip_lines")


class TripLinesTD(TypedDict):
    """TripLinesTD."""

    uuid: str
    source_uuid: str
    idx: str
    lines: list[IndexedStringTD]


@dataclass(slots=True)
class TripLines:
    """TripLines."""

    source_uuid: str
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
        """Make a uuid from a namespace and the repr of asdict(self), minus the uuid field."""
        return make_uuid_iter(indexed_strings=self.lines, namespace=TRIP_LINES_NS)

    @staticmethod
    def from_simple(simple_obj: TripLinesTD) -> "TripLines":
        """from_simple.

        Args:
            simple_obj (TripLinesTD): _description_

        Returns:
            TripLines: _description_
        """
        result = TripLines(
            uuid=simple_obj["uuid"],
            source_uuid=simple_obj["source_uuid"],
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
        return f"trip-lines_{idx}_{uuid}.json"


def trip_lines_serializer() -> DataclassSerializer[TripLines, TripLinesTD]:
    """trip_lines_serializer.

    Returns:
        DataclassSerializer[TripLines, TripLinesTD]: _description_
    """
    return DataclassSerializer[TripLines, TripLinesTD](
        complex_factory=TripLines.from_simple
    )


TRIP_LINES_SERIALIZER = trip_lines_serializer()


class TripLinesSaver:
    """TripLinesSaver."""

    def __init__(self, path_out: Path) -> None:
        """Save TripLines to a directory using the default file name.

        Args:
            path_out (Path): The directory to save the TripLines to.
        """
        if path_out.is_file():
            raise ValueError(
                f"Path out is an existing file, should be a directory. {path_out=}"
            )
        self.path_out = path_out

    def __call__(self, trip_lines: TripLines, overwrite: bool = False) -> Path:
        """Save TripLines to a directory using the default file name.

        Args:
            trip_lines (TripLines): The TripLines to save.
            overwrite (bool): Overwrite existing files.

        Returns:
            Path: The path to the saved file.
        """
        path_out = self.path_out / trip_lines.default_file_name()
        TRIP_LINES_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=trip_lines, overwrite=overwrite
        )
        return path_out


class TripLinesLoader(DataFileLoader[TripLines]):
    """TripLinesLoader."""

    def __init__(self, path_in: Path, glob: str = "trip-lines_*.json") -> None:
        """Load TripLines from directory.

        Args:
            path_in (Path): _description_
            glob (str, optional): _description_. Defaults to "trip-lines_*.json".
        """
        super().__init__(path_in, glob)

    def _translate(self, obj_path: Path) -> TripLines:
        return TRIP_LINES_SERIALIZER.load_from_json(path_in=obj_path)
