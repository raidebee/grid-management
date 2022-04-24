import pytest

from src.grid_management.common.models import Size
from src.grid_management.domain.models.grids import BoolGrid, ValueEmptyError
from src.grid_management.domain.models.grid_managements import GridManagement
from src.grid_management.domain.dependencies.grid_generators import (
    BoolGridGenerator,
)
from src.grid_management.domain.dependencies.grid_dot_managers import (
    BoolGridDotManager,
)
from src.grid_management.domain.dependencies.query_processors import (
    DummyQueryProcessor,
)


def test_grid_magenement_generate_dots():
    size = Size(height=3, width=3)

    grid = BoolGridGenerator(size).generate()
    dot_manager = BoolGridDotManager
    query_processor = DummyQueryProcessor(grid)

    management = GridManagement(grid, dot_manager, query_processor)

    assert management.generate_dots(3) == 3
    assert management.generate_dots(5) == 5
    assert management.generate_dots(5) == 1


def test_grid_magenement_remove_dots():
    size = Size(height=3, width=3)

    grid = BoolGridGenerator(size).generate()
    dot_manager = BoolGridDotManager
    query_processor = DummyQueryProcessor(grid)

    management = GridManagement(grid, dot_manager, query_processor)

    assert management.generate_dots(9) == 9
    assert management.remove_dots(5) == 5
    assert management.remove_dots(3) == 3
    assert management.remove_dots(3) == 1


def test_grid_get_size_normal():
    value = [[False, False], [False, False], [False, False]]

    grid = BoolGrid(value)

    assert grid.size.height == 3
    assert grid.size.width == 2


def test_grid_get_size_value_empty_error():
    grid = BoolGrid(None)

    with pytest.raises(ValueEmptyError):
        grid.size
