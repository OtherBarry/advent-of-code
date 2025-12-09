from collections import defaultdict

from solutions.base import BaseSolution
from solutions.utils.grid import BaseGrid, CharacterGrid, Coordinate, Direction

TURN_RIGHT = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}


def get_next_move(
    grid: BaseGrid[str], current: Coordinate, direction: Direction
) -> tuple[Coordinate, Direction]:
    while grid.get_value(forward := direction.apply(current)) == "#":
        direction = TURN_RIGHT[direction]
    return forward, direction


def results_in_loop_on_turn(
    grid: BaseGrid[str], start: Coordinate, direction: Direction
) -> bool:
    current = start
    path: dict[Coordinate, list[Direction]] = defaultdict(list)
    direction = TURN_RIGHT[direction]
    while current in grid:
        if direction in path[current]:
            return True
        path[current].append(direction)
        current, direction = get_next_move(grid, current, direction)
    return False


class Solution(BaseSolution):
    def setup(self) -> None:
        self.grid = CharacterGrid(self.raw_input)
        starting_position = None
        for coordinate in self.grid:
            if self.grid[coordinate] == "^":
                starting_position = coordinate
                break
        if starting_position is None:
            msg = "No starting position found"
            raise ValueError(msg)
        self.starting_position = starting_position

    def part_1(self) -> int:
        current = self.starting_position
        direction = Direction.UP
        visited = set()
        while current in self.grid:
            visited.add(current)
            current, direction = get_next_move(self.grid, current, direction)
        return len(visited)

    def part_2(self) -> int:
        return 0
