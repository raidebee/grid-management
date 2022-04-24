from abc import ABC, abstractmethod
import pickle

from src.grid_management.domain.models.grids import AbstractGrid


class AbstractGridManagementRepository(ABC):
    @abstractmethod
    def save(self, grid: AbstractGrid) -> None:
        raise NotImplementedError

    @abstractmethod
    def load(self) -> AbstractGrid:
        raise NotImplementedError


class GridManagementFileRepository(AbstractGridManagementRepository):
    def __init__(self, path: str) -> None:
        self.path = path

    def save(self, grid: AbstractGrid) -> None:
        self._grid = grid

    def load(self) -> AbstractGrid:
        with open(self.path, "rb") as file:
            return pickle.load(file)
