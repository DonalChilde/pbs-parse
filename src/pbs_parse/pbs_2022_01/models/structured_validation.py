"""Models used in validating trips."""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import TypedDict
from uuid import NAMESPACE_DNS, UUID, uuid5

from pfmsoft.simple_serializer import DataclassSerializer

from .parsed_trip import PARSED_TRIP_SERIALIZER, ParsedTrip, ParsedTripTD
from .structured import STRUCTURED_TRIP_SERIALIZER, StructuredTrip
from .structured_TD import StructuredTripTD

STRUCTURED_VALIDATION_NS = uuid5(
    NAMESPACE_DNS, "pbs_parse.pbs_2022_01.structured_validation"
)


class StructuredValidationTD(TypedDict):
    """A simple container for all the information required to validate a structured trip."""

    uuid: str
    parsed: ParsedTripTD
    structured: StructuredTripTD
    parsed_path: str
    structured_path: str
    valid_start_dates: list[str]
    errors: list[str]


@dataclass(slots=True)
class StructuredValidation:
    """A container for all the information required to validate a structured trip."""

    parsed: ParsedTrip
    structured: StructuredTrip
    parsed_path: str
    structured_path: str
    uuid: str = ""
    valid_start_dates: list[date] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        """Custom str output."""
        return (
            "StructuredValidation:\n"
            f"{self.parsed_path=}\n"
            f"{self.structured_path=}\n"
            f"{self.uuid=}\n"
            f"{self.valid_start_dates=!r}\n"
            f"\nErrors:\n{"\n".join(self.errors)}"
            f"\nParsed:\n{self.parsed}\n"
            f"\nStructured:\n{self.structured}\n"
            "\n"
        )

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
        """Make a uuid from a namespace and the source uuid as a string."""
        return uuid5(namespace=STRUCTURED_VALIDATION_NS, name=self.structured.uuid)

    def default_file_name(self) -> str:
        """Make a default file name."""
        structured_path = Path(self.structured.default_file_name())
        return f"{structured_path.stem}_errors.json"

    def to_simple(self) -> StructuredValidationTD:
        """Make a json serializable version."""
        simple = StructuredValidationTD(
            uuid=self.uuid,
            parsed=PARSED_TRIP_SERIALIZER.to_simple(self.parsed),
            structured=STRUCTURED_TRIP_SERIALIZER.to_simple(self.structured),
            parsed_path=self.parsed_path,
            structured_path=self.structured_path,
            valid_start_dates=[x.isoformat() for x in self.valid_start_dates],
            errors=self.errors,
        )
        return simple

    @staticmethod
    def from_simple(simple_obj: StructuredValidationTD) -> "StructuredValidation":
        """Convert from json to object."""
        result = StructuredValidation(
            parsed=PARSED_TRIP_SERIALIZER.from_simple(simple_obj=simple_obj["parsed"]),
            structured=STRUCTURED_TRIP_SERIALIZER.from_simple(
                simple_obj=simple_obj["structured"]
            ),
            parsed_path=simple_obj["parsed_path"],
            structured_path=simple_obj["structured_path"],
            valid_start_dates=[
                date.fromisoformat(x) for x in simple_obj["valid_start_dates"]
            ],
            errors=simple_obj["errors"],
        )
        return result


STRUCTURED_VALIDATION_SERIALIZER = DataclassSerializer[
    StructuredValidation, StructuredValidationTD
](
    complex_factory=StructuredValidation.from_simple,
    simple_factory=StructuredValidation.to_simple,
)
