from bisect import insort
from itertools import combinations

from shapely import Polygon

from solutions.base import BaseSolution
from solutions.utils.grid import Coordinate


def rectangle_area(tile_1: Coordinate, tile_2: Coordinate) -> int:
    return (abs(tile_1[0] - tile_2[0]) + 1) * (abs(tile_1[1] - tile_2[1]) + 1)


def get_polygon(tile_1: Coordinate, tile_2: Coordinate) -> Polygon:
    return Polygon((tile_1, (tile_1[0], tile_2[1]), tile_2, (tile_2[0], tile_1[1])))


class Solution(BaseSolution):
    def setup(self) -> None:
        self._tiles = []
        for line in self.raw_input.splitlines():
            x_str, y_str = line.split(",")
            self._tiles.append((int(x_str), int(y_str)))

        pairs: list[tuple[int, tuple[Coordinate, Coordinate]]] = []
        for pair in combinations(self._tiles, 2):
            area = rectangle_area(*pair)
            insort(pairs, (area, pair))

        self._pairs = pairs

    def part_1(self) -> int:
        area, _ = self._pairs[-1]
        return area

    def part_2(self) -> int:
        tiled_area = Polygon(self._tiles)
        for area, pair in reversed(self._pairs):
            polygon = get_polygon(*pair)
            if tiled_area.contains(polygon):
                return area

        raise ValueError("No valid rectangle found")
