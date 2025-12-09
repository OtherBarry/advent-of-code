from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid, Coordinate, Direction

SEARCH_VALUE = "XMAS"
VALID_X_MAS_BARS = ("SAM", "MAS")
X_MAS_CENTER = "A"


class Solution(BaseSolution):
    def setup(self) -> None:
        self.grid = CharacterGrid(self.raw_input)

    def is_search_value_in_direction(
        self, start: Coordinate, direction: Direction
    ) -> bool:
        current = start
        for character in SEARCH_VALUE:
            if self.grid.get_value(current) != character:
                return False
            current = direction.apply(current)
        return True

    def is_center_of_x_mas(self, start: Coordinate) -> bool:
        center = self.grid[start]
        top_left = (
            self.grid[Direction.UP_LEFT.apply(start)]
            + center
            + self.grid[Direction.DOWN_RIGHT.apply(start)]
        )
        if top_left not in VALID_X_MAS_BARS:
            return False
        bottom_left = (
            self.grid[Direction.DOWN_LEFT.apply(start)]
            + center
            + self.grid[Direction.UP_RIGHT.apply(start)]
        )
        return not bottom_left not in VALID_X_MAS_BARS

    def part_1(self) -> int:
        found_words = 0
        for coordinate in self.grid:
            if self.grid[coordinate] == SEARCH_VALUE[0]:
                found_words += sum(
                    self.is_search_value_in_direction(coordinate, direction)
                    for direction in Direction
                )
        return found_words

    def part_2(self) -> int:
        found_x_mas = 0
        for y in range(1, self.grid.height - 1):
            for x in range(1, self.grid.width - 1):
                if self.grid[(y, x)] == X_MAS_CENTER:
                    found_x_mas += int(self.is_center_of_x_mas((y, x)))
        return found_x_mas
