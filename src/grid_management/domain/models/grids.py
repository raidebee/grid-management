from abc import ABC, abstractmethod
from typing import Any

from src.grid_management.common.models import Size


class GridError(Exception):
    pass


class ValueEmptyError(GridError):
    pass


class AbstractGrid(ABC):
    def __init__(
        self,
        value: Any = None,
    ) -> None:
        self._value = value

    @property
    def value(self) -> Any:
        return self._value

    @property
    @abstractmethod
    def size(self) -> Size:
        pass


class BoolGrid(AbstractGrid):
    def __init__(
        self,
        value: list[list[bool]] | None = None,
    ) -> None:
        self._value = value

    @property
    def value(self) -> list[list[bool]] | None:
        return self._value

    @property
    def size(self) -> Size:
        if self.value is None:
            raise ValueEmptyError("Value must be set to get the size.")

        height = len(self.value)
        width = len(self.value[0])
        return Size(height, width)
