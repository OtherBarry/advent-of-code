from collections import Counter

from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid, Coordinate, Direction


class Solution(BaseSolution):
    def setup(self) -> None:
        self._grid = CharacterGrid(self.raw_input)
        start = None
        for coord, value in self._grid.enumerate():
            if value == "S":
                start = coord
                break

        if start is None:
            raise ValueError("Start position 'S' not found in the grid.")

        self._start = start

    def next_moves(self, pos: Coordinate) -> tuple[Coordinate, ...]:
        next_pos = Direction.DOWN.apply(pos)
        if self._grid[next_pos] == "^":
            return (Direction.LEFT.apply(next_pos), Direction.RIGHT.apply(next_pos))
        return (next_pos,)

    def part_1(self) -> int:
        split_count = 0
        beams = {self._start}
        for _ in range(self._grid.height - 1):
            new_beams: set[Coordinate] = set()
            for beam in beams:
                next_moves = self.next_moves(beam)
                if len(next_moves) > 1:
                    split_count += 1
                new_beams.update(next_moves)
            beams = new_beams
        return split_count

    def part_2(self) -> int:
        beams = Counter([self._start])
        for _ in range(self._grid.height - 1):
            new_beams: Counter[Coordinate] = Counter()
            for beam, count in beams.items():
                next_moves = self.next_moves(beam)
                for move in next_moves:
                    new_beams[move] += count
            beams = new_beams
        return sum(beams.values())
