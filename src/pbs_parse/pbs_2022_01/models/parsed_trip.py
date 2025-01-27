"""Models for Parsed trips."""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import TypedDict
from uuid import NAMESPACE_DNS, uuid5

from pfmsoft.indexed_string.model import IndexedStringTD
from pfmsoft.simple_serializer import DataclassSerializer
from pfmsoft.state_parser import model

from pbs_parse.pbs_2022_01.models.external_data import ExternalData, ExternalDataTD
from pbs_parse.snippets.file.data_file_loader import DataFileLoader

PARSED_TRIP_NS = uuid5(NAMESPACE_DNS, "pbs_parse.pbs_2022_01.parsed_trip")


class ParsedTripSourceTD(TypedDict):
    """ParsedTripSourceTD."""

    txt_file: str
    page_lines: str
    trip_lines: str


class ParsedTripTD(TypedDict):
    """A simple object version of ParsedTrip."""

    source: ParsedTripSourceTD
    external: ExternalDataTD
    idx: str
    parsed_lines: list[model.ParsedIndexedStringTD]
    calendar_entries: list[str]
    start_dates: list[str]
    errors: list[str]


@dataclass(slots=True)
class ParsedTripSource:
    """ParsedTripSource."""

    txt_file: str = "TXT_FILE"
    page_lines: str = "PAGE_LINES"
    trip_lines: str = "TRIP_LINES"

    @staticmethod
    def from_simple(value: ParsedTripSourceTD) -> "ParsedTripSource":
        """From simple."""
        return ParsedTripSource(
            txt_file=value["txt_file"],
            page_lines=value["page_lines"],
            trip_lines=value["trip_lines"],
        )

    def to_simple(self) -> ParsedTripSourceTD:
        """to_simple."""
        return ParsedTripSourceTD(
            txt_file=self.txt_file,
            page_lines=self.page_lines,
            trip_lines=self.trip_lines,
        )


@dataclass(slots=True)
class ParsedTrip:
    """ParsedTrip contains the parsed lines of a pbs trip."""

    source: ParsedTripSource
    external: ExternalData
    idx: str
    parsed_lines: list[model.ParsedIndexedString] = field(default_factory=list)
    calendar_entries: list[str] = field(default_factory=list)
    start_dates: list[date] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @staticmethod
    def from_simple(simple_obj: ParsedTripTD) -> "ParsedTrip":
        """Reconstitute a ParsedTrip from a simple object."""
        result = ParsedTrip(
            source=ParsedTripSource.from_simple(simple_obj["source"]),
            external=ExternalData.from_simple(simple_obj["external"]),
            idx=simple_obj["idx"],
            parsed_lines=[
                model.ParsedIndexedString.from_simple(x)
                for x in simple_obj["parsed_lines"]
            ],
            calendar_entries=[x for x in simple_obj["calendar_entries"]],
            start_dates=[date.fromisoformat(x) for x in simple_obj["start_dates"]],
            errors=[x for x in simple_obj["errors"]],
        )
        return result

    def to_simple(self) -> ParsedTripTD:
        """To_simple."""
        return ParsedTripTD(
            source=self.source.to_simple(),
            external=self.external.to_simple(),
            idx=self.idx,
            parsed_lines=[
                model.ParsedIndexedStringTD(
                    id=x.id,
                    indexed_string=IndexedStringTD(
                        idx=x.indexed_string.idx, txt=x.indexed_string.txt
                    ),
                    data=x.data,
                )
                for x in self.parsed_lines
            ],
            calendar_entries=[x for x in self.calendar_entries],
            start_dates=[x.isoformat() for x in self.start_dates],
            errors=[x for x in self.errors],
        )

    def default_file_name(self) -> str:
        """default_file_name.

        Args:
            page_idx (int): _description_
            trip_idx (int): _description_

        Returns:
            str: _description_
        """
        return self.assemble_file_name(idx=self.idx, external=self.external)

    @staticmethod
    def assemble_file_name(idx: str, external: ExternalData) -> str:
        """assemble_file_name.

        Args:
            idx (str): _description_
            external (ExternalData): _description_

        Returns:
            str: _description_
        """
        return f"parsed-trip_{external.base}_{external.effective_from}_{idx}.json"

    def original_text(self, with_line_num: bool = True, sep: str = "") -> str:
        """Get the original input text, with and without line numbers."""
        if with_line_num:
            return f"{sep.join([f'[{x.indexed_string.idx:06}] {x.indexed_string.txt}' for x in self.parsed_lines])}\n"
        else:
            return (
                f"{sep.join([f'{x.indexed_string.txt}' for x in self.parsed_lines])}\n"
            )

    def __str__(self) -> str:
        """Make a str rep of ParsedTrip."""
        return (
            "ParsedTrip:\n"
            f"{self.idx=}\n"
            f"{self.source=}\n"
            f"Errors: {len(self.errors)}\n"
            f"{"\n".join(self.errors)}"
            "\nText Input:\n"
            f"{self.original_text()}"
            "Parsed Data:\n"
            f"{'\n'.join([f'{x.id:20}[{x.indexed_string.idx:06}] {x.data!r}' for x in self.parsed_lines])}\n"
        )


def parsed_trip_serializer() -> DataclassSerializer[ParsedTrip, ParsedTripTD]:
    """Construct a serializer for Parsedtrip."""
    return DataclassSerializer[ParsedTrip, ParsedTripTD](
        complex_factory=ParsedTrip.from_simple, simple_factory=ParsedTrip.to_simple
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
