from __future__ import annotations
from abc import ABC, abstractmethod
import pickle

from src.grid_management.infrastructure.repositories import (
    AbstractGridManagementRepository,
    GridManagementFileRepository,
)


class AbstractGridManagementUnitOfWork(ABC):
    grid: AbstractGridManagementRepository

    def __enter__(self) -> AbstractGridManagementUnitOfWork:
        return self

    def __exit__(self, *args) -> None:
        self.rollback()

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass


class GridManagementFileUnitOfWork(AbstractGridManagementUnitOfWork):
    def __init__(self, path: str) -> None:
        self.path = path

    def __enter__(self) -> GridManagementFileUnitOfWork:
        self.grid = GridManagementFileRepository(self.path)
        return self

    def commit(self) -> None:
        with open(self.path, "wb") as file:
            pickle.dump(self.grid._grid, file)

    def rollback(self) -> None:
        pass
