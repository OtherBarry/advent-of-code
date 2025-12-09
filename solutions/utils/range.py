from typing import Self


class Range:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def __contains__(self, item: int) -> bool:
        return self.start <= item <= self.end

    def overlaps(self, other: Self) -> bool:
        return self.start <= other.end and other.start <= self.end

    def merge(self, other: Self) -> "Range":
        if not self.overlaps(other):
            raise ValueError("Ranges do not overlap and cannot be merged")
        return Range(min(self.start, other.start), max(self.end, other.end))

    def __repr__(self) -> str:
        return f"Range({self.start}, {self.end})"


def simplify_ranges(ranges: list[Range]) -> list[Range]:
    ranges.sort(key=lambda r: r.start)
    simplified = [ranges[0]]

    for current in ranges[1:]:
        last = simplified[-1]
        if last.overlaps(current):
            simplified[-1] = last.merge(current)
        else:
            simplified.append(current)

    return simplified
