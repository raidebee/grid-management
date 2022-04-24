from __future__ import annotations
import os
import pickle
from typing import Any

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
    GridManagementFileUnitOfWork,
)
from src.grid_management.application.services import generate_dots, remove_dots
from tests.utils import sum_after_flattening_list

GRID_MANAGEMENT_FILE_PATH = ".test_grid_management_data"


def teardown_module(module) -> None:
    delete_grid_file()


def save_grid_file(grid: AbstractGrid) -> None:
    with open(GRID_MANAGEMENT_FILE_PATH, "wb") as file:
        pickle.dump(grid, file)


def load_grid_file() -> AbstractGrid:
    with open(GRID_MANAGEMENT_FILE_PATH, "rb") as file:
        return pickle.load(file)


def delete_grid_file() -> None:
    if not os.path.exists(GRID_MANAGEMENT_FILE_PATH):
        return

    os.remove(GRID_MANAGEMENT_FILE_PATH)


def load_grid_value() -> Any:
    return load_grid_file().value


def test_generate_dots():
    size = Size(height=3, width=3)

    dot_manager = BoolGridDotManager
    grid = BoolGridGenerator(size).generate()
    query_processor = DummyQueryProcessor(grid)

    save_grid_file(grid)
    assert sum_after_flattening_list(load_grid_value()) == 0

    uow = GridManagementFileUnitOfWork(GRID_MANAGEMENT_FILE_PATH)

    with uow:
        assert generate_dots(3, dot_manager, query_processor, uow) == 3

    assert sum_after_flattening_list(load_grid_value()) == 3

    with uow:
        assert generate_dots(5, dot_manager, query_processor, uow) == 5

    assert sum_after_flattening_list(load_grid_value()) == 8

    with uow:
        assert generate_dots(5, dot_manager, query_processor, uow) == 1

    assert sum_after_flattening_list(load_grid_value()) == 9


def test_remove_dots():
    size = Size(height=3, width=3)

    dot_manager = BoolGridDotManager
    grid = BoolGridGenerator(size).generate()
    query_processor = DummyQueryProcessor(grid)

    save_grid_file(grid)
    assert sum_after_flattening_list(load_grid_value()) == 0

    uow = GridManagementFileUnitOfWork(GRID_MANAGEMENT_FILE_PATH)

    with uow:
        assert generate_dots(9, dot_manager, query_processor, uow) == 9

    assert sum_after_flattening_list(load_grid_value()) == 9

    with uow:
        assert remove_dots(5, dot_manager, query_processor, uow) == 5

    assert sum_after_flattening_list(load_grid_value()) == 4

    with uow:
        assert remove_dots(3, dot_manager, query_processor, uow) == 3

    assert sum_after_flattening_list(load_grid_value()) == 1

    with uow:
        assert remove_dots(3, dot_manager, query_processor, uow) == 1

    assert sum_after_flattening_list(load_grid_value()) == 0
