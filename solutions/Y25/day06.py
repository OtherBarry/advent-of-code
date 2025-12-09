from dataclasses import dataclass
from functools import reduce
from operator import add, mul

from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid, WhitespaceGrid

OPERAND_MAP = {"+": add, "*": mul}


@dataclass
class Problem:
    operands: list[int]
    operator: str

    def solve(self) -> int:
        operator_func = OPERAND_MAP[self.operator]
        return reduce(operator_func, self.operands)


class Solution(BaseSolution):
    def setup(self) -> None:
        pass

    def part_1(self) -> int:
        grid = WhitespaceGrid(self.raw_input)

        return sum(
            Problem(
                operands=[int(value) for value in column[:-1]], operator=column[-1]
            ).solve()
            for column in grid.iter_columns()
        )

    def part_2(self) -> int:
        grid = CharacterGrid(self.raw_input)
        operands: list[int] = []
        operator = None
        problems = []

        for column in reversed(list(grid.iter_columns())):
            raw_number = reduce(add, column).strip()
            if raw_number == "":
                if operator is None:
                    raise ValueError("Operator missing for problem")
                problems.append(Problem(operands=operands, operator=operator))
                operands = []
                operator = None
                continue
            if not raw_number.isdigit():
                operator = raw_number[-1]
                raw_number = raw_number[:-1].strip()

            operands.append(int(raw_number))

        if operator is None:
            raise ValueError("Operator missing for problem")
        problems.append(Problem(operands=operands, operator=operator))

        return sum(problem.solve() for problem in problems)
