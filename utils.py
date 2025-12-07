import tempfile
from importlib import import_module
from pathlib import Path
from typing import Literal

from solutions.base import BaseSolution


def get_solution_class(year: int, day: int) -> type[BaseSolution]:
    solution_module = import_module(f"solutions.Y{str(year)[-2:]}.day{day:02d}")
    return solution_module.Solution


def get_default_input_path(year: int, day: int) -> Path:
    return Path(f"inputs/Y{str(year)[-2:]}/{day:02d}.txt")


def get_solution_result(solution: BaseSolution, part: Literal[1, 2]) -> int:
    solution.setup()

    if part == 1:
        return solution.part_1()
    if part == 2:
        return solution.part_2()
    raise ValueError("Part must be 1 or 2")


def get_solution_with_default_path(year: int, day: int, part: Literal[1, 2]) -> int:
    input_path = Path(f"inputs/Y{str(year)[-2:]}/{day:02d}.txt")
    solution_class = get_solution_class(year, day)
    solution = solution_class(input_path)
    return get_solution_result(solution, part)


def get_solution_from_string(
    year: int, day: int, part: Literal[1, 2], input_string: str
) -> int:
    solution_class = get_solution_class(year, day)
    with tempfile.NamedTemporaryFile("w+") as temp_file:
        temp_file.write(input_string)
        temp_file.flush()
        temp_path = Path(temp_file.name)
        solution = solution_class(temp_path)
        return get_solution_result(solution, part)
