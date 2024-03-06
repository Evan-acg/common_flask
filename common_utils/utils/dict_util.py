from copy import deepcopy
from typing import Any, Dict


def clone_deep(o):
    """
    Creates a deep copy of the given object.

    Parameters:
        o (object): The object to be cloned.

    Returns:
        object: A deep copy of the given object.
    """
    return deepcopy(o)


def merge(*dicts: Dict[str, Any]) -> Dict:
    """
    Merge multiple dictionaries into a single dictionary.

    Args:
        *dicts: Variable number of dictionaries to be merged.

    Returns:
        dict: A dictionary containing the merged key-value pairs from all input dictionaries.

    Example:
        >>> dict1 = {'a': 1, 'b': 2}
        >>> dict2 = {'c': 3, 'd': 4}
        >>> dict3 = {'e': 5, 'f': 6}
        >>> merge(dict1, dict2, dict3)
        {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
    """
    for d in dicts:
        if not isinstance(d, dict):
            raise ValueError("All input arguments must be dictionaries.")
    ret: Dict[str, Any] = {}
    for d in dicts:
        for k, v in d.items():
            if isinstance(v, dict) and isinstance(ret.get(k), dict):
                ret[k] = merge(ret[k], v)
            else:
                ret[k] = v
    return ret
