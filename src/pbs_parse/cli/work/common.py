"""FILE: common.py."""

from dataclasses import dataclass


@dataclass(slots=True)
class KeyedResource[T]:
    """KeyedResource."""

    resource: T
    key: str
