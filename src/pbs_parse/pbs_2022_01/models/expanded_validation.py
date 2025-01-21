"""FILE: expanded_validation.py."""

from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict
from uuid import NAMESPACE_DNS, uuid5

from pfmsoft.simple_serializer import DataclassSerializer

from .expanded import EXPANDED_TRIP_SERIALIZER, ExpandedTrip
from .expanded_TD import ExpandedTripTD
from .parsed_trip import PARSED_TRIP_SERIALIZER, ParsedTrip, ParsedTripTD
from .structured import STRUCTURED_TRIP_SERIALIZER, StructuredTrip
from .structured_TD import StructuredTripTD

EXPANDED_VALIDATION_NS = uuid5(
    NAMESPACE_DNS, "pbs_parse.pbs_2022_01.expanded_validation"
)


class ExpandedValidationTD(TypedDict):
    """A simple container for all the information required to validate a structured trip."""

    expanded: ExpandedTripTD
    parsed: ParsedTripTD | None
    structured: StructuredTripTD
    parsed_path: str
    structured_path: str
    expanded_path: str


@dataclass(slots=True)
class ExpandedValidation:
    """A validator for expanded trips."""

    expanded: ExpandedTrip
    structured: StructuredTrip
    parsed: ParsedTrip | None = None
    expanded_path: str = ""
    structured_path: str = ""
    parsed_path: str = ""

    def __str__(self) -> str:
        """Custom str output."""
        return (
            "ExpandedValidation:\n"
            f"{self.parsed_path=}\n"
            f"{self.structured_path=}\n"
            f"{self.expanded_path=}\n"
            # f"{self.uuid=}\n"
            f"\nErrors:\n{"\n".join(self.expanded.errors)}\n"
            f"\n{self.parsed}\n"
            f"\nStructured:\n{self.structured}\n"
            f"\nExpanded:\n{self.expanded}\n"
            "\n"
        )

    # def make_uuid(self) -> UUID:
    #     """Make a uuid from a namespace and the expanded uuid."""
    #     return uuid5(namespace=EXPANDED_VALIDATION_NS, name=self.expanded.uuid)

    def default_file_name(self) -> str:
        """Make a default file name."""
        expanded_path = Path(self.expanded.default_file_name())
        return f"{expanded_path.stem}_errors.json"

    def to_simple(self) -> ExpandedValidationTD:
        """Make a json serializable version."""
        if self.parsed is not None:
            parsed = PARSED_TRIP_SERIALIZER.to_simple(self.parsed)
        else:
            parsed = self.parsed
        simple = ExpandedValidationTD(
            # uuid=self.uuid,
            expanded=EXPANDED_TRIP_SERIALIZER.to_simple(self.expanded),
            parsed=parsed,
            structured=STRUCTURED_TRIP_SERIALIZER.to_simple(self.structured),
            parsed_path=self.parsed_path,
            structured_path=self.structured_path,
            expanded_path=self.expanded_path,
            # errors=self.errors,
        )
        return simple

    @staticmethod
    def from_simple(simple_obj: ExpandedValidationTD) -> "ExpandedValidation":
        """Convert from json to object."""
        if simple_obj["parsed"] is not None:
            parsed = PARSED_TRIP_SERIALIZER.from_simple(simple_obj=simple_obj["parsed"])
        else:
            parsed = None
        result = ExpandedValidation(
            parsed=parsed,
            structured=STRUCTURED_TRIP_SERIALIZER.from_simple(
                simple_obj=simple_obj["structured"]
            ),
            expanded=EXPANDED_TRIP_SERIALIZER.from_simple(
                simple_obj=simple_obj["expanded"]
            ),
            expanded_path=simple_obj["expanded_path"],
            parsed_path=simple_obj["parsed_path"],
            structured_path=simple_obj["structured_path"],
            # errors=simple_obj["errors"],
        )
        return result


EXPANDED_VALIDATION_SERIALIZER = DataclassSerializer[
    ExpandedValidation, ExpandedValidationTD
](
    complex_factory=ExpandedValidation.from_simple,
    simple_factory=ExpandedValidation.to_simple,
)
