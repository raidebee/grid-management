from src.grid_management.domain.models.grids import AbstractGrid
from src.grid_management.domain.dependencies.grid_dot_managers import (
    AbstractGridDotManager,
)
from src.grid_management.domain.dependencies.query_processors import (
    AbstractQueryProcessor,
)


class GridManagement:
    def __init__(
        self,
        grid: AbstractGrid,
        dot_manager: AbstractGridDotManager,
        query_processor: AbstractQueryProcessor,
    ) -> None:
        self.grid = grid
        self.dot_manager = dot_manager
        self.query_processor = query_processor

    def generate_dots(self, number: int) -> int:
        coordinates = self.query_processor.pop_generatable_coordinates(number)
        for coordinate in coordinates:
            self.dot_manager.set_dot(self.grid, coordinate)
        return len(coordinates)

    def remove_dots(self, number: int) -> int:
        coordinates = self.query_processor.push_removable_coordinates(number)
        for coordinate in coordinates:
            self.dot_manager.unset_dot(self.grid, coordinate)
        return len(coordinates)
