import re

from solutions.base import BaseSolution

REGEX = r"mul\(\d+,\d+\)"


def parse_mul(mul: str) -> int:
    left, right = mul.split(",")
    return int(left[4:]) * int(right[:-1])


def execute_segment(segment: str) -> int:
    return sum(parse_mul(match) for match in re.findall(REGEX, segment))


class Solution(BaseSolution):
    def part_1(self) -> int:
        return execute_segment(self.raw_input)

    def part_2(self) -> int:
        total = 0
        remaining_text = self.raw_input
        while remaining_text:
            end = remaining_text.find("don't()")
            if end == -1:
                total += execute_segment(remaining_text)
                break

            total += execute_segment(remaining_text[:end])

            next_start = remaining_text.find("do()", end)
            if next_start == -1:
                break

            remaining_text = remaining_text[next_start + 4 :]

        return total
