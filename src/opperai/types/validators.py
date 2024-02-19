from functools import wraps
from typing import Callable


def validate_id_xor_path(func: Callable) -> Callable:
    """
    A decorator to validate that either 'id' or 'path' is provided as an argument.
    Raises ValueError if neither is provided.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "id" not in kwargs and "path" not in kwargs:
            raise ValueError("Either 'id' or 'path' must be provided as an argument.")
        elif "id" in kwargs and "path" in kwargs:
            raise ValueError(
                "Only one of 'id' or 'path' should be provided as an argument."
            )
        return func(*args, **kwargs)

    return wrapper
