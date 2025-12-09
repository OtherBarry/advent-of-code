import sys

import networkx as nx

from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid, Coordinate, Direction


def char_to_dir(char: str, direction: Direction) -> list[Direction]:  # noqa: PLR0911
    match (char, direction):
        # continue in same direction
        case (
            (".", _)
            | ("-", Direction.RIGHT)
            | ("-", Direction.LEFT)
            | ("|", Direction.UP)
            | ("|", Direction.DOWN)
        ):
            return [direction]

        # bounce off mirror
        case ("\\", Direction.RIGHT) | ("/", Direction.LEFT):
            return [Direction.DOWN]
        case ("\\", Direction.LEFT) | ("/", Direction.RIGHT):
            return [Direction.UP]
        case ("\\", Direction.UP) | ("/", Direction.DOWN):
            return [Direction.LEFT]
        case ("\\", Direction.DOWN) | ("/", Direction.UP):
            return [Direction.RIGHT]

        # split
        case ("-", Direction.UP) | ("-", Direction.DOWN):
            return [Direction.LEFT, Direction.RIGHT]
        case ("|", Direction.LEFT) | ("|", Direction.RIGHT):
            return [Direction.UP, Direction.DOWN]
        case _:
            msg = f"Invalid char/direction: {char}/{direction}"
            raise ValueError(msg)


class Solution(BaseSolution):
    def setup(self) -> None:
        self.map = CharacterGrid(self.raw_input)

        # this is almost certainly a sign of doing the wrong thing
        sys.setrecursionlimit((self.map.height * self.map.width) * 4)

    def count_energised_tiles(self, start_pos: Coordinate, start_dir: Direction) -> int:
        graph = nx.DiGraph()

        def update_graph(pos: Coordinate, direction: Direction) -> None:
            next_pos = direction.apply(pos)

            if graph.has_edge(pos, next_pos) or next_pos not in self.map:
                # next pos is out of bounds, or we've already visited it from this pos
                return
            graph.add_edge(pos, next_pos)
            char = self.map[next_pos]
            for new_dir in char_to_dir(char, direction):
                update_graph(next_pos, new_dir)

        update_graph(start_pos, start_dir)
        return graph.number_of_nodes()

    def part_1(self) -> int:
        return self.count_energised_tiles((0, 0), Direction.RIGHT)

    def part_2(self) -> int:
        height = self.map.height
        width = self.map.width
        most_illumination = 0
        for i in range(self.map.height):
            most_illumination = max(
                most_illumination,
                self.count_energised_tiles((i, 0), Direction.RIGHT),
                self.count_energised_tiles((i, width - 1), Direction.LEFT),
            )
        for j in range(self.map.width):
            most_illumination = max(
                most_illumination,
                self.count_energised_tiles((0, j), Direction.DOWN),
                self.count_energised_tiles((height - 1, j), Direction.UP),
            )
        return most_illumination
