from solutions.base import BaseSolution


class Solution(BaseSolution):
    def setup(self) -> None:
        self.elves = []
        elf = 0
        for line in self.raw_input.splitlines():
            if line == "":
                self.elves.append(elf)
                elf = 0
            else:
                elf += int(line)
        self.elves.sort(reverse=True)

    def part_1(self) -> int:
        return self.elves[0]

    def part_2(self) -> int:
        return sum(self.elves[:3])
