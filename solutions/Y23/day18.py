from collections.abc import Iterable

from shapely import Polygon

from solutions.base import BaseSolution
from solutions.utils.grid import Direction

DIR_LETTER_MAP = {
    "R": Direction.RIGHT,
    "L": Direction.LEFT,
    "U": Direction.UP,
    "D": Direction.DOWN,
}

DIR_DIGIT_MAP = {
    "0": Direction.RIGHT,
    "1": Direction.DOWN,
    "2": Direction.LEFT,
    "3": Direction.UP,
}


def calculate_area(data: Iterable[tuple[Direction, int]]) -> int:
    current = (0, 0)
    points = [current]
    for direction, distance in data:
        current = direction.apply(current, distance)
        points.append(current)

    polygon = Polygon(points)

    # Calculating grid points, not area
    return int(polygon.area + (polygon.length // 2) + 1)


def parse_hex(hex_code: str) -> tuple[Direction, int]:
    direction = DIR_DIGIT_MAP[hex_code[-1]]
    distance = int(hex_code[:-1], 16)
    return direction, distance


class Solution(BaseSolution):
    def setup(self) -> None:
        pass

    def part_1(self) -> int:
        data = []
        for line in self.raw_input.splitlines():
            dir_char, raw_distance, _ = line.split()
            data.append((DIR_LETTER_MAP[dir_char], int(raw_distance)))
        return calculate_area(data)

    def part_2(self) -> int:
        return calculate_area(
            parse_hex(line[-7:-1]) for line in self.raw_input.splitlines()
        )
