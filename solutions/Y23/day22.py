from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property

from solutions.base import BaseSolution


@dataclass
class Brick:
    x_range: tuple[int, int]
    y_range: tuple[int, int]
    z_range: tuple[int, int]

    @classmethod
    def from_line(cls, line: str) -> "Brick":
        """
        Parse a line from the input file into a Brick object.

        Example input:
        1,0,1~1,2,1
        Example output:
        Brick(x_range=(1, 1), y_range=(0, 2), z_range=(1, 1))
        """
        start, end = line.split("~")
        return cls(
            *zip(
                (int(v) for v in start.split(",")),
                (int(v) for v in end.split(",")),
                strict=True,
            )
        )

    @cached_property
    def xy_nodes(self) -> list[tuple[int, int]]:
        return [
            (x, y)
            for x in range(self.x_range[0], self.x_range[1] + 1)
            for y in range(self.y_range[0], self.y_range[1] + 1)
        ]

    def with_new_z(self, new_z: int) -> "Brick":
        diff = self.z_range[0] - new_z
        return Brick(
            x_range=self.x_range,
            y_range=self.y_range,
            z_range=(self.z_range[0] - diff, self.z_range[1] - diff),
        )


def settle_bricks(bricks: list[Brick]) -> tuple[list[Brick], int]:
    moved_bricks = 0
    lowest_bricks: dict[tuple[int, int], int] = defaultdict(int)
    new_bricks = []
    for brick in sorted(bricks, key=lambda b: b.z_range[0]):
        new_z = max(lowest_bricks[(x, y)] for x, y in brick.xy_nodes) + 1
        new_brick = brick.with_new_z(new_z)
        for x, y in brick.xy_nodes:
            lowest_bricks[(x, y)] = new_brick.z_range[1]
        new_bricks.append(new_brick)
        if new_brick != brick:
            moved_bricks += 1
    return new_bricks, moved_bricks


class Solution(BaseSolution):
    def setup(self) -> None:
        self.p1_result = 0
        self.p2_result = 0
        bricks, _ = settle_bricks(
            [Brick.from_line(line) for line in self.raw_input.splitlines()]
        )
        for i in range(len(bricks)):
            _, moved_bricks = settle_bricks(bricks[:i] + bricks[i + 1 :])
            if moved_bricks == 0:
                self.p1_result += 1
            self.p2_result += moved_bricks

    def part_1(self) -> int:
        return self.p1_result

    def part_2(self) -> int:
        return self.p2_result
