from __future__ import annotations
from typing import Any
import copy

from src.grid_management.common.models import Size
from src.grid_management.domain.models.grids import AbstractGrid
from src.grid_management.domain.dependencies.grid_generators import (
    BoolGridGenerator,
)
from src.grid_management.domain.dependencies.grid_dot_managers import (
    BoolGridDotManager,
)
from src.grid_management.domain.dependencies.query_processors import (
    DummyQueryProcessor,
)
from src.grid_management.application.unit_of_works import (
    AbstractGridManagementUnitOfWork,
)
from src.grid_management.infrastructure.repositories import (
    AbstractGridManagementRepository,
)
from src.grid_management.application.services import generate_dots, remove_dots
from tests.utils import sum_after_flattening_list


class FakeGridManagementFileRepository(AbstractGridManagementRepository):
    def __init__(self, grid=None) -> None:
        self._grid = grid

    def save(self, grid: AbstractGrid) -> None:
        self._grid = copy.deepcopy(grid)

    def load(self) -> AbstractGrid:
        return self._grid


class FakeGridManagementFileUnitOfWork(AbstractGridManagementUnitOfWork):
    def __init__(self) -> None:
        self.grid = FakeGridManagementFileRepository()
        self.committed = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass


def load_grid_value(uow: AbstractGridManagementUnitOfWork) -> Any:
    return uow.grid.load().value


def test_generate_dots():
    size = Size(height=3, width=3)

    dot_manager = BoolGridDotManager

    uow = FakeGridManagementFileUnitOfWork()

    grid = BoolGridGenerator(size).generate()
    uow.grid.save(grid)

    query_processor = DummyQueryProcessor(grid)

    assert generate_dots(3, dot_manager, query_processor, uow) == 3
    assert uow.committed
    assert sum_after_flattening_list(load_grid_value(uow)) == 3

    assert generate_dots(5, dot_manager, query_processor, uow) == 5
    assert sum_after_flattening_list(load_grid_value(uow)) == 8

    assert generate_dots(5, dot_manager, query_processor, uow) == 1
    assert sum_after_flattening_list(load_grid_value(uow)) == 9


def test_remove_dots():
    size = Size(height=3, width=3)

    dot_manager = BoolGridDotManager

    uow = FakeGridManagementFileUnitOfWork()

    grid = BoolGridGenerator(size).generate()
    uow.grid.save(grid)

    query_processor = DummyQueryProcessor(grid)

    assert generate_dots(9, dot_manager, query_processor, uow) == 9
    assert uow.committed
    assert sum_after_flattening_list(load_grid_value(uow)) == 9

    assert remove_dots(5, dot_manager, query_processor, uow) == 5
    assert sum_after_flattening_list(load_grid_value(uow)) == 4

    assert remove_dots(3, dot_manager, query_processor, uow) == 3
    assert sum_after_flattening_list(load_grid_value(uow)) == 1

    assert remove_dots(3, dot_manager, query_processor, uow) == 1
    assert sum_after_flattening_list(load_grid_value(uow)) == 0
