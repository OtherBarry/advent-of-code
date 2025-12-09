from solutions.base import BaseSolution


def check_report(level: list[int]) -> bool:
    increasing = level[0] < level[-1]
    for i in range(1, len(level)):
        difference = level[i] - level[i - 1]
        if increasing != (difference > 0):
            return False
        if not 0 < abs(difference) < 4:
            return False
    return True


def check_report_with_dampener(level: list[int]) -> bool:
    return any(check_report(level[:i] + level[i + 1 :]) for i in range(len(level)))


class Solution(BaseSolution):
    def setup(self) -> None:
        self.reports = [
            [int(x) for x in line.split()] for line in self.raw_input.splitlines()
        ]

    def part_1(self) -> int:
        return sum(map(check_report, self.reports))

    def part_2(self) -> int:
        return sum(map(check_report_with_dampener, self.reports))
