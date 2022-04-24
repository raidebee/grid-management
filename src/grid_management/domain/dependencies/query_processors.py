from abc import ABC, abstractmethod
import random

from src.grid_management.common.models import Coordinate
from src.grid_management.domain.models.grids import AbstractGrid


class AbstractQueryProcessor(ABC):
    def __init__(self, grid: AbstractGrid) -> None:
        self.grid = grid

    @abstractmethod
    def pop_generatable_coordinates(self, number: int) -> list[Coordinate]:
        pass

    @abstractmethod
    def push_removable_coordinates(self, number: int) -> list[Coordinate]:
        pass


class DummyQueryProcessor(AbstractQueryProcessor):
    def __init__(self, grid: AbstractGrid, is_shuffled=True) -> None:
        self.grid = grid
        self.is_shuffled = is_shuffled

        self._initialize_indexes()

    def _initialize_indexes(self) -> None:
        self._indexes = list(range(self.grid.size.width * self.grid.size.height))
        if self.is_shuffled:
            random.shuffle(self._indexes)

        self._current_index = 0

    def _convert_index_to_coordinate(self, index: int) -> Coordinate:
        y = index // self.grid.size.width
        x = index % self.grid.size.width
        return Coordinate(y, x)

    def _convert_indexes_to_coordinates(self, indexes: list[int]) -> list[Coordinate]:
        return [self._convert_index_to_coordinate(index) for index in indexes]

    def pop_generatable_coordinates(self, number: int) -> list[Coordinate]:
        if self._current_index >= len(self._indexes):
            return []

        last_index = min(self._current_index + number - 1, len(self._indexes) - 1)
        indexes = self._indexes[self._current_index : last_index + 1]
        self._current_index = last_index + 1
        return self._convert_indexes_to_coordinates(indexes)

    def push_removable_coordinates(self, number: int) -> list[Coordinate]:
        if self._current_index == 0:
            return []

        first_index = max(self._current_index - number, 0)
        indexes = self._indexes[first_index : self._current_index]
        self._current_index = first_index
        return self._convert_indexes_to_coordinates(indexes)
