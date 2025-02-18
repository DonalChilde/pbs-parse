"""Utility functionsfor working with IndexedStrings."""

from uuid import NAMESPACE_DNS, UUID, uuid5

from .model import IndexedStringProtocol, IndexedStringTD


def make_uuid5(
    indexed_string: IndexedStringProtocol, namespace: UUID = NAMESPACE_DNS
) -> UUID:
    """Make a uuid from one IndexedString."""
    string_value = f"{indexed_string.idx}: {indexed_string.txt}"
    return uuid5(namespace=namespace, name=string_value)


def make_uuid5_dict(
    indexed_string_td: IndexedStringTD, namespace: UUID = NAMESPACE_DNS
) -> UUID:
    """Make a uuid from one IndexedString."""
    string_value = f"{indexed_string_td['idx']}: {indexed_string_td['txt']}"
    return uuid5(namespace=namespace, name=string_value)
