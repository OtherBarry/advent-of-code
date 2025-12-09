from collections.abc import Sequence

from solutions.base import BaseSolution
from solutions.utils.grid import IntegerGrid
from solutions.utils.ints import concatenate


def get_max_digit_and_index(digits: Sequence[int]) -> tuple[int, int]:
    max_value = digits[0]
    max_index = 0
    for i in range(1, len(digits)):
        if digits[i] > max_value:
            max_value = digits[i]
            max_index = i
    return max_index, max_value


def biggest_number_from_digits(digits: Sequence[int], n: int) -> int:
    search_range = len(digits) - n + 1
    index, value = get_max_digit_and_index(digits[:search_range])
    if n == 1:
        return value
    return concatenate(value, biggest_number_from_digits(digits[index + 1 :], n - 1))


class Solution(BaseSolution):
    def setup(self) -> None:
        self._banks = list(IntegerGrid(self.raw_input).iter_rows())

    def part_1(self) -> int:
        return sum(biggest_number_from_digits(row, 2) for row in self._banks)

    def part_2(self) -> int:
        return sum(biggest_number_from_digits(row, 12) for row in self._banks)
