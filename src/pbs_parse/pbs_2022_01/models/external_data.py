"""FILE: external_data.py."""

from dataclasses import dataclass
from datetime import date
from typing import TypedDict


class ExternalDataTD(TypedDict):
    """ExternalDataTD."""

    base: str
    effective_from: str
    effective_to: str


@dataclass(slots=True)
class ExternalData:
    """ExternalData."""

    base: str = "BASE"
    effective_from: date = date(1900, 1, 1)
    effective_to: date = date(1900, 1, 2)

    def to_simple(self) -> ExternalDataTD:
        """To simple."""
        return ExternalDataTD(
            base=self.base,
            effective_from=self.effective_from.isoformat(),
            effective_to=self.effective_to.isoformat(),
        )

    @staticmethod
    def from_simple(value: ExternalDataTD) -> "ExternalData":
        """From simple."""
        return ExternalData(
            base=value["base"],
            effective_from=date.fromisoformat(value["effective_from"]),
            effective_to=date.fromisoformat(value["effective_to"]),
        )
