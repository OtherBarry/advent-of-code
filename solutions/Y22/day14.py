from contextlib import suppress

from solutions.base import BaseSolution


class SandGrain:
    def __init__(self, max_y: int) -> None:
        self.coordinates = (500, 0)
        self.max_y = max_y

    def coordinates_in_bounds(self, y: int) -> bool:
        return 0 <= y <= self.max_y

    def move_once(self, blocked_coordinates: set[tuple[int, int]]) -> bool:
        x, y = self.coordinates
        for move in (
            (x, y + 1),  # Down
            (x - 1, y + 1),  # Down left
            (x + 1, y + 1),  # Down right
        ):
            if not self.coordinates_in_bounds(move[1]):
                raise ValueError("Sand grain has fallen out of bounds")
            if move not in blocked_coordinates:
                self.coordinates = move
                return True
        return False

    def move(self, valid_coordinates: set[tuple[int, int]]) -> None:
        while self.move_once(valid_coordinates):
            pass


class Solution(BaseSolution):
    def setup(self) -> None:
        values = []
        max_y = 0
        for line in self.raw_input.splitlines():
            line_values = []
            for coordinate_pair in line.split(" -> "):
                coordinates = tuple(int(c) for c in coordinate_pair.split(","))
                max_y = max(max_y, coordinates[1])
                line_values.append(coordinates)
            values.append(line_values)
        blocked_coordinates = set()
        for row in values:
            for i in range(1, len(row)):
                start = row[i - 1]
                end = row[i]
                if start[0] == end[0]:
                    for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                        blocked_coordinates.add((start[0], y))
                elif start[1] == end[1]:
                    for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                        blocked_coordinates.add((x, start[1]))
        self.blocked_coordinates = blocked_coordinates
        self.max_y = max_y

    def part_1(self) -> int:
        blocked_coordinates = self.blocked_coordinates.copy()
        count = 0
        while True:
            count += 1
            grain = SandGrain(self.max_y)
            try:
                grain.move(blocked_coordinates)
            except ValueError:
                return count - 1
            blocked_coordinates.add(grain.coordinates)

    def part_2(self) -> int:
        blocked_coordinates = self.blocked_coordinates.copy()
        count = 0
        while True:
            count += 1
            grain = SandGrain(self.max_y + 1)

            with suppress(ValueError):
                grain.move(blocked_coordinates)

            blocked_coordinates.add(grain.coordinates)
            if grain.coordinates == (500, 0):
                return count
