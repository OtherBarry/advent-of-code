from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid


class Solution(BaseSolution):
    def setup(self) -> None:
        self._grid = CharacterGrid(self.raw_input)

    def is_accessible(self, coord: tuple[int, int]) -> bool:
        count = 0
        for neighbor in self._grid.neighbours(coord):
            if self._grid[neighbor] == "@":
                if count == 3:
                    return False
                count += 1
        return True

    def part_1(self) -> int:
        return sum(
            1
            for coord in self._grid
            if self._grid[coord] == "@" and self.is_accessible(coord)
        )

    def part_2(self) -> int:
        total_accessible = 0
        for _ in range(self._grid.height * self._grid.width):  # Max iterations
            found_accessible = 0
            for coord in self._grid:
                if self._grid[coord] == "@" and self.is_accessible(coord):
                    found_accessible += 1
                    self._grid[coord] = "."
            if found_accessible == 0:
                break
            total_accessible += found_accessible
        return total_accessible
