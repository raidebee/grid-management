from abc import ABC, abstractmethod
from typing import Any

from src.grid_management.common.models import Coordinate
from src.grid_management.domain.models.grids import AbstractGrid, BoolGrid
from src.grid_management.constants import BOOL_OCCUPIED_MARK, BOOL_EMPTY_MARK


class GridDotManagerError(Exception):
    pass


class OutOfRangeError(GridDotManagerError):
    pass


class AlreadyEmptyError(GridDotManagerError):
    pass


class AlreadyOccupiedError(GridDotManagerError):
    pass


class AbstractGridDotManager(ABC):
    @classmethod
    def set_dot(cls, grid: AbstractGrid, coordinate: Coordinate) -> None:
        cls._validate_range(grid, coordinate)
        cls._validate_if_empty(grid, coordinate)

        cls._set_dot(grid, coordinate)

    @classmethod
    def unset_dot(cls, grid: AbstractGrid, coordinate: Coordinate) -> None:
        cls._validate_range(grid, coordinate)
        cls._validate_if_occupied(grid, coordinate)

        cls._unset_dot(grid, coordinate)

    @classmethod
    def get_dot(cls, grid: AbstractGrid, coordinate: Coordinate) -> Any:
        cls._validate_range(grid, coordinate)

        return cls._get_dot(grid, coordinate)

    @classmethod
    @abstractmethod
    def _set_dot(cls, grid: AbstractGrid, coordinate: Coordinate) -> None:
        pass

    @classmethod
    @abstractmethod
    def _unset_dot(cls, grid: AbstractGrid, coordinate: Coordinate) -> None:
        pass

    @classmethod
    @abstractmethod
    def _get_dot(cls, grid: AbstractGrid, coordinate: Coordinate) -> Any:
        pass

    @classmethod
    @abstractmethod
    def _validate_range(cls, grid: AbstractGrid, coordinate: Coordinate) -> None:
        pass

    @classmethod
    @abstractmethod
    def _validate_if_empty(cls, grid: AbstractGrid, coordinate: Coordinate) -> None:
        pass

    @classmethod
    @abstractmethod
    def _validate_if_occupied(cls, grid: AbstractGrid, coordinate: Coordinate) -> None:
        pass


class BoolGridDotManager(AbstractGridDotManager):
    OCCUPIED_MARK = BOOL_OCCUPIED_MARK
    EMPTY_MARK = BOOL_EMPTY_MARK

    @classmethod
    def _set_dot(cls, grid: BoolGrid, coordinate: Coordinate) -> None:
        grid.value[coordinate.y][coordinate.x] = cls.OCCUPIED_MARK

    @classmethod
    def _unset_dot(cls, grid: BoolGrid, coordinate: Coordinate) -> None:
        grid.value[coordinate.y][coordinate.x] = cls.EMPTY_MARK

    @classmethod
    def _get_dot(cls, grid: BoolGrid, coordinate: Coordinate) -> bool:
        return grid.value[coordinate.y][coordinate.x]

    @classmethod
    def _validate_range(cls, grid: BoolGrid, coordinate) -> None:
        if coordinate.y >= grid.size.height:
            raise OutOfRangeError(
                f"y({coordinate.y}) must be less than the height of grid({grid.size.height})."
            )
        if coordinate.x >= grid.size.width:
            raise OutOfRangeError(
                f"x({coordinate.x}) must be less than the width of grid({grid.size.width})."
            )

    @classmethod
    def _validate_if_occupied(cls, grid: BoolGrid, coordinate: Coordinate) -> None:
        if cls.get_dot(grid, coordinate) == cls.EMPTY_MARK:
            raise AlreadyEmptyError(f"{coordinate} has already been empty.")

    @classmethod
    def _validate_if_empty(cls, grid: BoolGrid, coordinate: Coordinate) -> None:
        if cls.get_dot(grid, coordinate) == cls.OCCUPIED_MARK:
            raise AlreadyOccupiedError(f"{coordinate} has already been occupied.")
