"""Models used in validating trips."""

from dataclasses import asdict, dataclass, field
from datetime import date
from pprint import pformat

from .expanded import ExpandedTrip
from .parsed_trip import ParsedTrip
from .structured import StructuredTrip


@dataclass(slots=True)
class StructuredValidation:
    """A container for all the information required to validate a structured trip."""

    parsed_trip: ParsedTrip
    structured_trip: StructuredTrip
    parsed_path: str
    structured_path: str
    external_start_dates: list[date] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        """Custom str output."""
        return (
            f"parsed_path: {self.parsed_path}\nstructured path: {self.structured_path}\n"
            f"external_start_dates: {self.external_start_dates!r}\n"
            f"{self.parsed_trip}\n\n{self.structured_trip}\n\n{"\n".join(self.errors)}"
        )


@dataclass(slots=True, kw_only=True)
class ExpandedValidation:
    """A container for all the information required to validate an expanded trip."""

    errors: list[str] = field(default_factory=list)
    expanded_trip: ExpandedTrip
    structured_trip: StructuredTrip
    expanded_path: str
    structured_path: str

    def __str__(self) -> str:
        """Custom str output."""
        return (
            f"Errors:/n{"\n".join(self.errors)}"
            f"\nexpanded_path: {self.expanded_path}\nstructured path: {self.structured_path}\n"
            f"{self.expanded_trip}\n\n{pformat(asdict(self.structured_trip),sort_dicts=False)}"
        )
