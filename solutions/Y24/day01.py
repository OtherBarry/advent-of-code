from collections import Counter

from solutions.base import BaseSolution


class Solution(BaseSolution):
    def setup(self) -> None:
        self.left = []
        self.right = []
        for line in self.raw_input.splitlines():
            left, right = line.split("   ")
            self.left.append(int(left))
            self.right.append(int(right))

    def part_1(self) -> int:
        pairs = zip(sorted(self.left), sorted(self.right), strict=True)
        return sum(abs(right - left) for left, right in pairs)

    def part_2(self) -> int:
        left_counter = Counter(self.left)
        right_counter = Counter(self.right)

        return sum(
            left_key * left_value * right_counter[left_key]
            for left_key, left_value in left_counter.items()
        )
