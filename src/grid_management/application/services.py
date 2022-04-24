from src.grid_management.domain.models.grid_managements import GridManagement
from src.grid_management.domain.dependencies.grid_dot_managers import (
    AbstractGridDotManager,
)
from src.grid_management.domain.dependencies.query_processors import (
    AbstractQueryProcessor,
)
from src.grid_management.application.unit_of_works import (
    AbstractGridManagementUnitOfWork,
)


def generate_dots(
    number: int,
    dot_manager: AbstractGridDotManager,
    query_processor: AbstractQueryProcessor,
    uow: AbstractGridManagementUnitOfWork,
) -> int:
    with uow:
        grid = uow.grid.load()

        management = GridManagement(grid, dot_manager, query_processor)
        number_of_generated_dots = management.generate_dots(number)

        uow.grid.save(grid)
        uow.commit()

    return number_of_generated_dots


def remove_dots(
    number: int,
    dot_manager: AbstractGridDotManager,
    query_processor: AbstractQueryProcessor,
    uow: AbstractGridManagementUnitOfWork,
) -> int:
    with uow:
        grid = uow.grid.load()

        management = GridManagement(grid, dot_manager, query_processor)
        number_of_removed_dots = management.remove_dots(number)

        uow.grid.save(grid)
        uow.commit()

    return number_of_removed_dots
