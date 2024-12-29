"""Models for Parsed trips."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict
from uuid import NAMESPACE_DNS, UUID, uuid5

from pfmsoft.simple_serializer import DataclassSerializer
from pfmsoft.state_parser import model

from pbs_parse.snippets.file.data_file_loader import DataFileLoader

PARSED_TRIP_NS = uuid5(NAMESPACE_DNS, "pbs_parse.pbs_2022_01.parsed_trip")


class ParsedTripTD(TypedDict):
    """A simple object version of ParsedTrip."""

    uuid: str
    source: str
    page_idx: int
    trip_idx: int
    parsed_lines: list[model.ParsedIndexedStringTD]


@dataclass(slots=True)
class ParsedTrip:
    """ParsedTrip contains the parsed lines of a pbs trip."""

    source: str
    page_idx: int
    trip_idx: int
    uuid: str = ""
    parsed_lines: list[model.ParsedIndexedString] = field(default_factory=list)

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
        return uuid5(namespace=PARSED_TRIP_NS, name=self.source)

    @staticmethod
    def from_simple(simple_obj: ParsedTripTD) -> "ParsedTrip":
        """Reconstitute a ParsedTrip from a simple object."""
        result = ParsedTrip(
            uuid=simple_obj["uuid"],
            source=simple_obj["source"],
            page_idx=simple_obj["page_idx"],
            trip_idx=simple_obj["trip_idx"],
            parsed_lines=[
                model.ParsedIndexedString.from_simple(x)
                for x in simple_obj["parsed_lines"]
            ],
        )
        return result

    def default_file_name(self) -> str:
        """default_file_name.

        Args:
            page_idx (int): _description_
            trip_idx (int): _description_

        Returns:
            str: _description_
        """
        return f"parsed-trip_page_{self.page_idx}_trip_{self.trip_idx}_{self.uuid}.json"

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


class ParsedTripSaver:
    """ParsedTripSaver."""

    def __init__(self, path_out: Path) -> None:
        """Save ParsedTrip to a directory using the default file name.

        Args:
            path_out (Path): The directory to save the ParsedTrip to.
        """
        if path_out.is_file():
            raise ValueError(
                f"Path out is an existing file, should be a directory. {path_out=}"
            )
        self.path_out = path_out

    def __call__(self, parsed_trip: ParsedTrip, overwrite: bool = False) -> Path:
        """Save ParsedTrip to a directory using the default file name.

        Args:
            parsed_trip (ParsedTrip): The ParsedTrip to save.
            overwrite (bool): Overwrite existing files.

        Returns:
            Path: The path to the saved file.
        """
        path_out = self.path_out / parsed_trip.default_file_name()
        PARSED_TRIP_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=parsed_trip, overwrite=overwrite
        )
        return path_out


class ParsedTripLoader(DataFileLoader[ParsedTrip]):
    """ParsedTripLoader."""

    def __init__(self, path_in: Path, glob: str = "parsed-trip_*.json") -> None:
        """Load ParsedTrip from directory.

        Args:
            path_in (Path): The directory to load files from.
            glob (str, optional): The glob to match files. Defaults to "parsed-trip_*.json".
        """
        super().__init__(path_in, glob)

    def _translate(self, obj_path: Path) -> ParsedTrip:
        return PARSED_TRIP_SERIALIZER.load_from_json(path_in=obj_path)
