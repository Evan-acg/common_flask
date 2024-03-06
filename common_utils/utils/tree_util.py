"""
This module provides utility functions for working with tree-like structures.

The main function in this module is `from_list`,
which converts a list of items into a tree-like structure based on the specified keys.
"""

from typing import Any, Dict, List, Protocol, cast


class T(Protocol):
    """A protocol representing a type with keys."""

    def keys(self) -> List[str]:
        """Return a list of keys."""


def from_list(
    items: List[T],
    primary_key: str = "id",
    parent_key: str = "pid",
    children_key: str = "children",
) -> List[T]:
    """
    Converts a list of items into a tree-like structure based on the specified keys.

    Args:
        items (List[T]): The list of items to convert into a tree structure.
        primary_key (str, optional): The key representing the primary identifier of each item. Defaults to "id".
        parent_key (str, optional): The key representing the parent identifier of each item. Defaults to "pid".
        children_key (str, optional): The key representing the children of each item. Defaults to "children".

    Returns:
        List[T]: The list of items organized in a tree-like structure.
    """
    _items = [dict(cast(Dict[str, Any], item)) for item in items]
    _mapping: Dict[str | None, List[Any]] = {}

    for item in _items:
        _mapping.setdefault(item.get(parent_key), []).append(item)

    for item in _items:
        matched = _mapping.get(item.get(primary_key), [])
        item.setdefault(children_key, matched)

    return _mapping.get("", []) + _mapping.get(None, [])
