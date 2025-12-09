from collections.abc import Iterable
from dataclasses import dataclass
from math import prod

from solutions.base import BaseSolution

InclusiveRange = tuple[int, int]


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_line(cls, line: str) -> "Part":
        return cls(
            **{k: int(v) for k, v in (s.split("=") for s in line[1:-1].split(","))}
        )

    @property
    def rating(self) -> int:
        return self.x + self.m + self.a + self.s


@dataclass
class Operation:
    property: str
    greater_than: bool
    value: int
    result: str

    def passes(self, part: Part) -> bool:
        part_value = getattr(part, self.property)
        if self.greater_than:
            return part_value > self.value
        return part_value < self.value

    @classmethod
    def from_line(cls, line: str) -> "Operation":
        col_index = line.index(":")
        return cls(
            property=line[0],
            greater_than=line[1] == ">",
            value=int(line[2:col_index]),
            result=line[col_index + 1 :],
        )

    def split_range(
        self, range_: InclusiveRange
    ) -> tuple[InclusiveRange | None, InclusiveRange | None]:
        """
        Split a range into two ranges, one that passes the operation and one that fails it.

        :param range_: The range to split
        :return: The passing range and the failing range in that order
        """
        if self.greater_than:
            if range_[0] > self.value:
                # lower bound is greater than value, passing=range, failing=None
                return range_, None
            if range_[1] < self.value:
                # upper bound is less than value, passing=None, failing=range
                return None, range_
            # value is in range, passing=(value+1, upper bound), failing=(lower bound, value)
            return (self.value + 1, range_[1]), (range_[0], self.value)

        if range_[1] < self.value:
            # upper bound is less than value, passing=range, failing=None
            return range_, None
        if range_[0] > self.value:
            # lower bound is greater than value, passing=None, failing=range
            return None, range_
        # value is in range, passing=(lower bound, value-1), failing=(value, upper bound)
        return (range_[0], self.value - 1), (self.value, range_[1])


@dataclass
class Filter:
    name: str
    operations: list[Operation]
    catch_all: str

    @classmethod
    def from_line(cls, line: str) -> "Filter":
        name, filters = line.replace("}", "").split("{")
        *raw_operations, catch_all = filters.split(",")
        operations = [Operation.from_line(operation) for operation in raw_operations]
        return cls(name, operations, catch_all)

    def apply(self, part: Part) -> str:
        for operation in self.operations:
            if operation.passes(part):
                return operation.result
        return self.catch_all


class FilterSet:
    def __init__(self, filters: Iterable[Filter]) -> None:
        self.filters = {f.name: f for f in filters}

    def process(self, part: Part) -> bool:
        current = self.filters["in"]
        result = current.apply(part)
        while result not in ("A", "R"):
            current = self.filters[result]
            result = current.apply(part)
        return result == "A"

    def _calculate_possibilities(
        self, filter_name: str, ranges: dict[str, InclusiveRange]
    ) -> int:
        if filter_name == "A":
            return prod((max_ - min_) + 1 for min_, max_ in ranges.values())
        if filter_name == "R":
            return 0
        filter_ = self.filters[filter_name]
        possibilities = 0
        for operation in filter_.operations:
            passing_range, failing_range = operation.split_range(
                ranges[operation.property]
            )
            if passing_range is None:
                continue

            new_ranges = ranges.copy()
            new_ranges[operation.property] = passing_range
            possibilities += self._calculate_possibilities(operation.result, new_ranges)
            if failing_range is None:
                return possibilities
            ranges[operation.property] = failing_range

        possibilities += self._calculate_possibilities(filter_.catch_all, ranges.copy())
        return possibilities

    def calculate_possibilities(self) -> int:
        return self._calculate_possibilities(
            "in", {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
        )


class Solution(BaseSolution):
    def setup(self) -> None:
        filter_lines, part_lines = self.raw_input.split("\n\n")
        self.filter_set = FilterSet(
            Filter.from_line(line) for line in filter_lines.splitlines()
        )
        self.parts = [Part.from_line(line) for line in part_lines.splitlines()]

    def part_1(self) -> int:
        return sum(part.rating for part in self.parts if self.filter_set.process(part))

    def part_2(self) -> int:
        return self.filter_set.calculate_possibilities()
