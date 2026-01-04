import string
from itertools import batched

from solutions.base import BaseSolution

PRIORITY_MAP = {
    char: priority for priority, char in enumerate(string.ascii_letters, start=1)
}


class Solution(BaseSolution):
    def setup(self) -> None:
        self.packs = [
            [PRIORITY_MAP[c] for c in line] for line in self.raw_input.splitlines()
        ]

    def part_1(self) -> int:
        result = 0
        for pack in self.packs:
            midpoint = len(pack) // 2
            intersection = set(pack[:midpoint]) & set(pack[midpoint:])
            result += intersection.pop()
        return result

    def part_2(self) -> int:
        result = 0
        for chunk in batched(self.packs, 3, strict=True):
            a, b, c = chunk
            intersection = set(a) & set(b) & set(c)
            result += intersection.pop()
        return result
