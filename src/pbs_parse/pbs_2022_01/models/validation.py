"""Models used in validating structured trips."""

from dataclasses import dataclass, field
from datetime import date

from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.structured import StructuredTrip


@dataclass(slots=True)
class Context:
    """A container for all the information required to validate a structured trip."""

    parsed_trip: ParsedTrip
    structured_trip: StructuredTrip
    external_start_dates: list[date] = field(default_factory=list)
    parsed_path: str = ""
    structured_path: str = ""
    errors: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        """Custom str output."""
        return (
            f"parsed_path: {self.parsed_path}\nstructured path: {self.structured_path}\n"
            f"external_start_dates: {self.external_start_dates!r}\n"
            f"{self.parsed_trip}\n\n{self.structured_trip}\n\n{"\n".join(self.errors)}"
        )
