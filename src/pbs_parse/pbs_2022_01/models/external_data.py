"""FILE: external_data.py."""

from dataclasses import dataclass
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
    effective_from: str = "EFFECTIVE_FROM"
    effective_to: str = "EFFECTIVE_TO"
