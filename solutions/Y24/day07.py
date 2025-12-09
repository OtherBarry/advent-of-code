from collections.abc import Callable, Iterable
from operator import add, mul

from solutions.base import BaseSolution
from solutions.utils.ints import concatenate

Operator = Callable[[int, int], int]


def is_equation_solvable_from_point(
    operators: Iterable[Operator],
    answer: int,
    values: list[int],
    current: int,
    index: int,
) -> bool:
    if index == len(values):
        return current == answer
    next_value = values[index]
    for operator in operators:
        next_current = operator(current, next_value)
        if next_current <= answer and is_equation_solvable_from_point(
            operators, answer, values, next_current, index + 1
        ):
            return True
    return False


def equation_can_be_solved(
    operators: Iterable[Operator], values: list[int], answer: int
) -> bool:
    return is_equation_solvable_from_point(operators, answer, values, values[0], 1)


class Solution(BaseSolution):
    def setup(self) -> None:
        self.equations = []
        for line in self.raw_input.splitlines():
            raw_answer, raw_values = line.split(":")
            self.equations.append(
                (int(raw_answer), [int(x) for x in raw_values.split()])
            )

    def part_1(self) -> int:
        operators = (add, mul)
        return sum(
            answer
            for answer, values in self.equations
            if equation_can_be_solved(operators, values, answer)
        )

    def part_2(self) -> int:
        operators = (add, mul, concatenate)
        return sum(
            answer
            for answer, values in self.equations
            if equation_can_be_solved(operators, values, answer)
        )
