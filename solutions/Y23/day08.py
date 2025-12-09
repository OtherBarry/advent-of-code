from collections.abc import Callable
from math import lcm

from solutions.base import BaseSolution


class Node:
    def __init__(self, value: str) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


def calculate_number_of_moves(
    start: Node, moves: str, is_end_node: Callable[[str], bool]
) -> int:
    current = start
    move_count = 0
    while not is_end_node(current.value):
        next_move = moves[move_count % len(moves)]
        current = current.left if next_move == "L" else current.right  # type: ignore[assignment]
        move_count += 1
    return move_count


class Solution(BaseSolution):
    def setup(self) -> None:
        lines = self.raw_input.splitlines()
        self.nodes: dict[str, Node] = {}
        for line in lines[2:]:
            node = self.nodes.setdefault(line[:3], Node(line[:3]))
            node.left = self.nodes.setdefault(line[7:10], Node(line[7:10]))
            node.right = self.nodes.setdefault(line[12:15], Node(line[12:15]))
        self.moves = lines[0]

    def part_1(self) -> int:
        return calculate_number_of_moves(
            self.nodes["AAA"], self.moves, lambda x: x == "ZZZ"
        )

    def part_2(self) -> int:
        return lcm(
            *(
                calculate_number_of_moves(node, self.moves, lambda x: x[-1] == "Z")
                for value, node in self.nodes.items()
                if value[-1] == "A"
            )
        )
