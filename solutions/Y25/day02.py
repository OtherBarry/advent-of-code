from collections.abc import Iterable
from itertools import batched, groupby
from typing import Any

from solutions.base import BaseSolution


def all_equal(iterable: Iterable[Any]) -> bool:
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


class Solution(BaseSolution):
    def setup(self) -> None:
        self._ranges = []
        for line in self.raw_input.split(","):
            start_str, end_str = line.split("-")
            while len(start_str) != len(end_str):
                self._ranges.append((int(start_str), int("9" * len(start_str))))
                start_str = str(int("1" + "0" * (len(start_str))))
            self._ranges.append((int(start_str), int(end_str)))

    def part_1(self) -> int:
        invalid_ids = []
        for start, end in self._ranges:
            length = len(str(start))
            if length % 2 != 0:
                continue
            midpoint = length // 2
            for id_ in range(start, end + 1):
                str_id = str(id_)
                for i in range(midpoint):
                    if str_id[i] != str_id[i + midpoint]:
                        break
                else:
                    invalid_ids.append(id_)
        return sum(invalid_ids)

    def part_2(self) -> int:
        invalid_ids = []
        for start, end in self._ranges:
            length = len(str(start))
            valid_group_sizes = [
                size for size in range(1, (length // 2) + 1) if length % size == 0
            ]
            for id_ in range(start, end + 1):
                str_id = str(id_)
                for size in reversed(valid_group_sizes):
                    batch = batched(str_id, n=size, strict=True)
                    if all_equal(batch):
                        invalid_ids.append(id_)
                        break
        return sum(invalid_ids)
