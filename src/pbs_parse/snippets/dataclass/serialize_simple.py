"""


ref: https://github.com/jeremander/fancy-dataclass/blob/main/fancy_dataclass/dict.py
"""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, is_dataclass  # noqa: F401
from typing import Any, Self


class DictConvertible(ABC):
    """Mixin class enabling conversion of an object to/from a Python dict.

    Subclasses should override `to_dict` and `from_dict` to implement the conversion."""

    @abstractmethod
    def to_dict(self, **kwargs: Any) -> dict[str, Any]:
        """Converts an object to a dict.

        Args:
            kwargs: Keyword arguments

        Returns:
            A Python dict"""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any], **kwargs: Any) -> Self:
        """Constructs an object from a dictionary of (attribute, value) pairs.

        Args:
            data: Dict to convert into an object
            kwargs: Keyword arguments

        Returns:
            Converted object of this class"""


class DictableDataclass(DictConvertible):
    def to_dict(self, **kwargs: Any) -> dict[str, Any]:
        return asdict(self)  # type: ignore

    @classmethod
    def from_dict(cls, data: dict[str, Any], **kwargs: Any) -> Self:
        return cls(**data)
