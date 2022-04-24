import itertools
from typing import Any


def flatten_list(value: list) -> list[Any]:
    return list(itertools.chain.from_iterable(value))
