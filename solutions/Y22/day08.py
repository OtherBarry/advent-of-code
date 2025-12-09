import numpy as np

from solutions.base import BaseSolution


def test_array_visibility(array: np.ndarray, mask: np.ndarray) -> None:
    current_max = -1
    for i, v in enumerate(array):
        if v > current_max:
            current_max = v
            mask[i] = True
    current_max = -1
    for i, v in reversed(list(enumerate(array))):
        if v > current_max:
            current_max = v
            mask[i] = True


def determine_visibility(array: np.ndarray, coordinates: tuple[int, int]) -> int:
    results = []
    value = array[coordinates]
    for direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        visibility = 0
        next_coordinates = coordinates
        while True:
            next_coordinates = tuple(np.add(next_coordinates, direction))
            if not all(0 <= c < 99 for c in next_coordinates):
                break
            visibility += 1
            if array[next_coordinates] >= value:
                break
        if visibility == 0:
            return 0
        results.append(visibility)
    return int(np.prod(results))


class Solution(BaseSolution):
    def setup(self) -> None:
        grid = [[int(char) for char in line] for line in self.raw_input.splitlines()]
        self.grid = np.asarray(grid, dtype=np.uint8)

    def part_1(self) -> int:
        binary_map = np.zeros(self.grid.shape, dtype=np.bool)
        for i in range(99):
            test_array_visibility(self.grid[i], binary_map[i])
            test_array_visibility(self.grid[:, i], binary_map[:, i])
        return int(np.sum(binary_map))

    def part_2(self) -> int:
        visibility_map = np.zeros(self.grid.shape, dtype=np.uint32)
        for (x, y), _ in np.ndenumerate(self.grid):
            visibility_map[x, y] = determine_visibility(self.grid, (x, y))
        return int(np.max(visibility_map))
