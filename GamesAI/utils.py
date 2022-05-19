from enum import Enum
from typing import Iterable, Callable

class Constant(Enum):
    DRAW = "DRAW"
    RANDOM = "RANDOM"
    
def argmax(indexes : Iterable, func : Callable, return_value : bool = False) -> object:
    """Return the object in values with the highest function.
    indexes : an iterable of indexes to consider.
    func : a function taking an index as argument and returning a value."""
    if len(indexes) == 0:
        raise ValueError("No element in indexes")
    max_value = float("-inf")
    for idx in indexes:
        value = func(idx)
        if value > max_value:
            max_value = value
            max_idx = idx
    if return_value: return max_idx, max_value
    return max_idx

def argmin(indexes : Iterable, func : Callable, return_value : bool = False) -> object:
    """Return the object in values with the highest function.
    indexes : an iterable of indexes to consider.
    func : a function taking an index as argument and returning a value."""
    if not return_value:
        return argmax(indexes, lambda idx : -func(idx))
    else:
        idx_min, minus_value_min = argmax(indexes, lambda idx : -func(idx), return_value = True)
        return idx_min, -minus_value_min