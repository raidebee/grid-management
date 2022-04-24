from abc import ABC, abstractmethod
from typing import Any

from src.grid_management.common.models import Size
from src.grid_management.domain.models.grids import AbstractGrid, BoolGrid


class AbstractGridGenerator(ABC):
    def __init__(self, size: Size, initial_dot_value: Any = None) -> None:
        self.size = size
        self.initial_dot_value = initial_dot_value

    @abstractmethod
    def generate(self) -> AbstractGrid:
        pass


class BoolGridGenerator(AbstractGridGenerator):
    def __init__(self, size: Size, initial_dot_value: bool = False) -> None:
        self.size = size
        self.initial_dot_value = initial_dot_value

    def generate(self) -> BoolGrid:
        value = [
            [self.initial_dot_value for _ in range(self.size.width)]
            for _ in range(self.size.height)
        ]
        return BoolGrid(value)
