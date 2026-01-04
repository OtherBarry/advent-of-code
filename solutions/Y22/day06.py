from collections import deque

from solutions.base import BaseSolution


def is_full_and_unique(stack: deque[str]) -> bool:
    return len(set(stack)) == stack.maxlen


class Solution(BaseSolution):
    def setup(self) -> None:
        pass

    def get_index_of_first_n_unique_chars(self, n: int) -> int:
        stack: deque[str] = deque(maxlen=n)
        for i, v in enumerate(self.raw_input):
            stack.append(v)
            if is_full_and_unique(stack):
                return i + 1
        raise ValueError("No unique sequence found")

    def part_1(self) -> int:
        return self.get_index_of_first_n_unique_chars(4)

    def part_2(self) -> int:
        return self.get_index_of_first_n_unique_chars(14)
