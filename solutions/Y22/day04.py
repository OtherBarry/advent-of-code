from solutions.base import BaseSolution
from solutions.utils.range import Range


class Solution(BaseSolution):
    def setup(self) -> None:
        pairs = []
        for line in self.raw_input.splitlines():
            pair = []
            for elf in line.split(","):
                start, end = elf.split("-")
                pair.append(Range(int(start), int(end)))
            pairs.append(pair)
        self.pairs = pairs

    def part_1(self) -> int:
        result = 0
        for a, b in self.pairs:
            if a in b or b in a:
                result += 1
        return result

    def part_2(self) -> int:
        result = 0
        for a, b in self.pairs:
            if a.overlaps(b):
                result += 1
        return result
