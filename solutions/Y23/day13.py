from itertools import chain

import numpy as np
import numpy.typing as npt

from solutions.base import BaseSolution

Pattern = npt.NDArray[np.bool_]


def pattern_to_np_array(pattern: str) -> Pattern:
    return np.array(
        [[c == "#" for c in row] for row in pattern.splitlines()], dtype=np.bool_
    )


def find_reflection(values: Pattern, expected_differences: int = 0) -> int | None:
    midpoint = len(values) // 2
    index = 1
    for window in chain(range(1, midpoint + 1), range(midpoint, 0, -1)):
        left = values[index - window : index]
        right = values[index : index + window][::-1]
        if np.sum(np.bitwise_xor(left, right)) == expected_differences:
            return index
        index += 1
    return None


def calculate_summary(pattern: Pattern, expected_differences: int = 0) -> int:
    if (column := find_reflection(pattern.T, expected_differences)) is not None:
        return column
    if (row := find_reflection(pattern, expected_differences)) is not None:
        return row * 100
    raise ValueError


class Solution(BaseSolution):
    def setup(self) -> None:
        self.patterns = [pattern_to_np_array(p) for p in self.raw_input.split("\n\n")]

    def part_1(self) -> int:
        return sum(calculate_summary(pattern) for pattern in self.patterns)

    def part_2(self) -> int:
        return sum(
            calculate_summary(pattern, expected_differences=1)
            for pattern in self.patterns
        )
