import operator
from bisect import insort
from dataclasses import dataclass
from functools import reduce
from itertools import combinations

from solutions.base import BaseSolution


@dataclass(frozen=True)
class Coordinate3D:
    x: int
    y: int
    z: int

    @classmethod
    def from_line(cls, line: str) -> "Coordinate3D":
        x_str, y_str, z_str = line.split(",")
        return cls(x=int(x_str), y=int(y_str), z=int(z_str))


def euclidean_distance(coord1: Coordinate3D, coord2: Coordinate3D) -> float:
    return (
        (coord1.x - coord2.x) ** 2
        + (coord1.y - coord2.y) ** 2
        + (coord1.z - coord2.z) ** 2
    ) ** 0.5


class Solution(BaseSolution):
    def setup(self) -> None:
        self._junction_box_coordinates = [
            Coordinate3D.from_line(line) for line in self.raw_input.splitlines()
        ]
        pairs: list[tuple[float, tuple[Coordinate3D, Coordinate3D]]] = []
        for pair in combinations(self._junction_box_coordinates, 2):
            distance = euclidean_distance(pair[0], pair[1])
            insort(pairs, (distance, pair))

        self._pairs = pairs

    def connect_pair(self, coord_1: Coordinate3D, coord_2: Coordinate3D) -> None:
        coord_1_circuit_index = None
        coord_2_circuit_index = None
        for index, circuit in enumerate(self._circuits):
            if coord_1 in circuit:
                coord_1_circuit_index = index
            if coord_2 in circuit:
                coord_2_circuit_index = index
            if coord_1_circuit_index is not None and coord_2_circuit_index is not None:
                break

        if coord_1_circuit_index is None and coord_2_circuit_index is None:
            self._circuits.append({coord_1, coord_2})
        elif coord_1_circuit_index == coord_2_circuit_index:
            return
        elif coord_1_circuit_index is not None and coord_2_circuit_index is not None:
            self._circuits[coord_1_circuit_index].update(
                self._circuits[coord_2_circuit_index]
            )
            del self._circuits[coord_2_circuit_index]
        elif coord_1_circuit_index is not None:
            self._circuits[coord_1_circuit_index].add(coord_2)
        elif coord_2_circuit_index is not None:
            self._circuits[coord_2_circuit_index].add(coord_1)

    def part_1(self) -> int:
        self._circuits: list[set[Coordinate3D]] = []

        for _ in range(1000):
            __, (coord_1, coord_2) = self._pairs.pop(0)
            self.connect_pair(coord_1, coord_2)

        self._circuits.sort(key=len, reverse=True)

        return reduce(operator.mul, map(len, self._circuits[:3]))

    def part_2(self) -> int:
        while len(self._pairs) > 0:
            __, (coord_1, coord_2) = self._pairs.pop(0)
            self.connect_pair(coord_1, coord_2)
            if len(self._circuits) == 1 and all(
                coord in self._circuits[0] for coord in self._junction_box_coordinates
            ):
                return coord_1.x * coord_2.x

        raise ValueError("No solution found")
