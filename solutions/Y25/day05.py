from solutions.base import BaseSolution
from solutions.utils.range import Range


class Solution(BaseSolution):
    def setup(self) -> None:
        range_input, id_input = self.raw_input.split("\n\n", maxsplit=1)
        ranges = []
        for line in range_input.splitlines():
            first, second = line.split("-")
            ranges.append(Range(int(first), int(second)))

        # Merge overlapping ranges
        ranges.sort(key=lambda r: r.start)
        self._ranges = []
        i = 0
        while i < len(ranges):
            step = 1
            range_ = ranges[i]
            for j in range(i + 1, len(ranges)):
                if ranges[j].overlaps(range_):
                    range_ = range_.merge(ranges[j])
                    step += 1
                else:
                    break
            i += step
            self._ranges.append(range_)

        self._ids = [int(line) for line in id_input.splitlines()]
        self._ids.sort()

    def part_1(self) -> int:
        return sum(
            1 for id_value in self._ids if any(id_value in r for r in self._ranges)
        )

    def part_2(self) -> int:
        return sum((range_.end - range_.start) + 1 for range_ in self._ranges)
