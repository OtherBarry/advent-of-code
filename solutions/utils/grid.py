from collections.abc import Iterator, MutableSequence, Sequence
from copy import deepcopy
from enum import Enum
from typing import Self

Coordinate = tuple[int, int]


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (-1, 1)
    DOWN_LEFT = (1, -1)
    DOWN_RIGHT = (1, 1)

    @classmethod
    def from_coordinates(cls, start: Coordinate, end: Coordinate) -> Self:
        return cls((end[0] - start[0], end[1] - start[1]))

    def apply(self, coordinate: Coordinate, distance: int = 1) -> Coordinate:
        return coordinate[0] + (self.value[0] * distance), coordinate[1] + (
            self.value[1] * distance
        )

    def __neg__(self) -> Self:
        return Direction((-self.value[0], -self.value[1]))


BASE_DIRECTIONS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
ALL_DIRECTIONS = [
    Direction.UP,
    Direction.UP_RIGHT,
    Direction.RIGHT,
    Direction.DOWN_RIGHT,
    Direction.DOWN,
    Direction.DOWN_LEFT,
    Direction.LEFT,
    Direction.UP_LEFT,
]


class BaseGrid[T]:
    def __init__(self, grid: Sequence[MutableSequence[T]]) -> None:
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def __getitem__(self, coordinate: Coordinate) -> T:
        y, x = coordinate
        return self.grid[y][x]

    def __setitem__(self, key: Coordinate, value: T) -> None:
        y, x = key
        self.grid[y][x] = value

    def __iter__(self) -> Iterator[Coordinate]:
        for y in range(self.height):
            for x in range(self.width):
                yield y, x

    def __contains__(self, coordinate: Coordinate) -> bool:
        return 0 <= coordinate[0] < self.height and 0 <= coordinate[1] < self.width

    def enumerate(self) -> Iterator[tuple[Coordinate, T]]:
        for coordinate in self:
            yield coordinate, self[coordinate]

    def get_value(self, coordinate: Coordinate) -> T | None:
        if coordinate not in self:
            return None
        return self[coordinate]

    def copy(self) -> "BaseGrid[T]":
        return BaseGrid(deepcopy(self.grid))

    def iter_rows(self) -> Iterator[Sequence[T]]:
        yield from self.grid

    def iter_columns(self) -> Iterator[Sequence[T]]:
        for x in range(self.width):
            yield [self.grid[y][x] for y in range(self.height)]

    def neighbours(
        self, coordinate: Coordinate, include_diagonal: bool = True
    ) -> Iterator[Coordinate]:
        directions = ALL_DIRECTIONS if include_diagonal else BASE_DIRECTIONS
        for direction in directions:
            neighbour = direction.apply(coordinate)
            if neighbour in self:
                yield neighbour


class CharacterGrid(BaseGrid[str]):
    def __init__(self, raw_input: str) -> None:
        super().__init__([list(line) for line in raw_input.splitlines()])

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.grid)


class IntegerGrid(BaseGrid[int]):
    def __init__(self, raw_input: str) -> None:
        super().__init__(
            [[int(char) for char in line] for line in raw_input.splitlines()]
        )


class WhitespaceGrid(BaseGrid[str]):
    def __init__(self, raw_input: str) -> None:
        super().__init__([line.split() for line in raw_input.splitlines()])


def manhattan_distance(a: Coordinate, b: Coordinate) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
