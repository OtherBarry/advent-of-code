from collections.abc import MutableSequence

import numpy as np
import numpy.typing as npt

from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid


def tilt_row(row: MutableSequence[str]) -> None:
    next_best_pos = 0
    for i in range(len(row)):
        match row[i]:
            case "O":
                row[i] = "."
                row[next_best_pos] = "O"
                next_best_pos += 1
            case "#":
                next_best_pos = i + 1


class Mirror:
    def __init__(self, mirror: npt.NDArray[str], rotations: int = 2) -> None:  # type: ignore[type-var]
        self._mirror = mirror
        self._rotations = rotations

    def normal_form(self) -> "Mirror":
        rotations = self._rotations % 4
        return Mirror(np.rot90(self._mirror, k=-rotations), 0)

    @classmethod
    def from_str(cls, s: str) -> "Mirror":
        mirror = np.array(CharacterGrid(s).grid)
        return cls(np.rot90(mirror, k=2))

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self._mirror)

    def tilt(self) -> "Mirror":
        mirror = self.rotate()
        for row in mirror._mirror:  # noqa: SLF001
            tilt_row(row)
        return mirror

    def rotate(self) -> "Mirror":
        return Mirror(np.rot90(self._mirror, k=-1), self._rotations - 1)

    def cycle(self) -> "Mirror":
        return self.tilt().tilt().tilt().tilt()

    def run_cycles(self, n_iters: int) -> "Mirror":
        mirror = self
        history = {mirror: 0}
        for i in range(1, n_iters + 1):
            mirror = mirror.cycle()
            if mirror in history:
                start = history[mirror]
                remaining_iters = n_iters - i
                cycle_length = i - start
                future_iters = remaining_iters % cycle_length
                for _ in range(future_iters):
                    mirror = mirror.cycle()
                return mirror
            history[mirror] = i
        return mirror

    def calculate_load(self) -> int:
        return sum(
            sum(len(col) - i for i, char in enumerate(col) if char == "O")
            for col in self._mirror
        )

    def matches(self, other: npt.NDArray[str]) -> bool:  # type: ignore[type-var]
        return np.array_equal(self._mirror, other)

    def __hash__(self) -> int:
        return hash(self._mirror.tobytes())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mirror):
            return NotImplemented
        return other.matches(self._mirror)


class Solution(BaseSolution):
    def setup(self) -> None:
        self.mirror = Mirror.from_str(self.raw_input)

    def part_1(self) -> int:
        return self.mirror.tilt().calculate_load()

    def part_2(self) -> int:
        return self.mirror.run_cycles(1_000_000_000).rotate().calculate_load()
