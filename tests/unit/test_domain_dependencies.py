import pytest

from src.grid_management.common.models import Size, Coordinate
from src.grid_management.domain.dependencies.grid_generators import (
    BoolGridGenerator,
)
from src.grid_management.domain.dependencies.grid_dot_managers import (
    BoolGridDotManager,
    OutOfRangeError,
    AlreadyEmptyError,
    AlreadyOccupiedError,
)
from src.grid_management.domain.dependencies.query_processors import (
    DummyQueryProcessor,
)


def test_grid_dot_manager_set_normal():
    size = Size(height=3, width=3)

    grid = BoolGridGenerator(size).generate()
    dot_manager = BoolGridDotManager

    assert dot_manager.get_dot(grid, Coordinate(0, 0)) == dot_manager.EMPTY_MARK
    dot_manager.set_dot(grid, Coordinate(0, 0))
    assert dot_manager.get_dot(grid, Coordinate(0, 0)) == dot_manager.OCCUPIED_MARK


def test_grid_dot_manager_raise_out_of_range_error():
    size = Size(height=3, width=3)

    grid = BoolGridGenerator(size).generate()
    dot_manager = BoolGridDotManager

    with pytest.raises(OutOfRangeError):
        dot_manager.set_dot(grid, Coordinate(3, 3))

    with pytest.raises(OutOfRangeError):
        dot_manager.get_dot(grid, Coordinate(3, 3))


def test_grid_dot_manager_raise_already_empty_error():
    size = Size(height=3, width=3)

    grid = BoolGridGenerator(size).generate()
    dot_manager = BoolGridDotManager

    with pytest.raises(AlreadyEmptyError):
        dot_manager.unset_dot(grid, Coordinate(0, 0))


def test_grid_dot_manager_raise_already_occupied_error():
    size = Size(height=3, width=3)

    grid = BoolGridGenerator(size).generate()
    dot_manager = BoolGridDotManager

    dot_manager.set_dot(grid, Coordinate(0, 0))

    with pytest.raises(AlreadyOccupiedError):
        dot_manager.set_dot(grid, Coordinate(0, 0))


def test_grid_generator():
    size = Size(height=3, width=3)

    grid = BoolGridGenerator(size).generate()
    assert grid.value == [
        [False, False, False],
        [False, False, False],
        [False, False, False],
    ]

    grid = BoolGridGenerator(size, True).generate()
    assert grid.value == [
        [True, True, True],
        [True, True, True],
        [True, True, True],
    ]


def test_query_processor():
    size = Size(height=3, width=3)

    grid = BoolGridGenerator(size).generate()

    query_processor = DummyQueryProcessor(grid)

    assert len(query_processor.pop_generatable_coordinates(5)) == 5
    assert len(query_processor.pop_generatable_coordinates(3)) == 3
    assert len(query_processor.pop_generatable_coordinates(3)) == 1
    assert len(query_processor.push_removable_coordinates(5)) == 5
    assert len(query_processor.push_removable_coordinates(3)) == 3
    assert len(query_processor.push_removable_coordinates(3)) == 1
