from itertools import combinations

from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid, Coordinate


def get_empty_rows_and_columns(grid: CharacterGrid) -> tuple[set[int], set[int]]:
    empty_rows = {
        i
        for i, row in enumerate(grid.iter_rows())
        if all(value == "." for value in row)
    }
    empty_columns = {
        i
        for i, col in enumerate(grid.iter_columns())
        if all(value == "." for value in col)
    }
    return empty_rows, empty_columns


class Solution(BaseSolution):
    def count_steps(self, start: Coordinate, end: Coordinate) -> tuple[int, int]:
        steps = 0
        empty_steps = 0
        for y in range(min(start[0], end[0]), max(start[0], end[0])):
            if y in self.empty_rows:
                empty_steps += 1
            else:
                steps += 1
        for x in range(min(start[1], end[1]), max(start[1], end[1])):
            if x in self.empty_columns:
                empty_steps += 1
            else:
                steps += 1
        return steps, empty_steps

    def setup(self) -> None:
        base_map = CharacterGrid(self.raw_input)
        self.empty_rows, self.empty_columns = get_empty_rows_and_columns(base_map)

        self.galaxies = []
        for coordinate, value in base_map.enumerate():
            if value == "#":
                self.galaxies.append(coordinate)

        self.num_steps = 0
        self.num_empty_steps = 0
        for start, end in combinations(self.galaxies, 2):
            steps, empty_steps = self.count_steps(start, end)
            self.num_steps += steps
            self.num_empty_steps += empty_steps

    def part_1(self) -> int:
        return self.num_steps + (self.num_empty_steps * 2)

    def part_2(self) -> int:
        return self.num_steps + (self.num_empty_steps * 1_000_000)
