from collections import deque
from collections.abc import Generator, Iterable
from copy import deepcopy
from dataclasses import dataclass

from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid


class Stack:
    def __init__(self, items: Iterable[str]) -> None:
        self._deque = deque(items)

    def pop(self, n: int = 1) -> Generator[str]:
        for _ in range(n):
            yield self._deque.popleft()

    def push(self, items: Iterable[str]) -> None:
        self._deque.extendleft(items)

    def peek(self) -> str:
        return self._deque[0]


@dataclass
class Move:
    source: int
    target: int
    count: int

    def perform(self, stacks: list[Stack]) -> None:
        stacks[self.target].push(stacks[self.source].pop(self.count))

    def perform_bulk(self, stacks: list[Stack]) -> None:
        stacks[self.target].push(reversed(list(stacks[self.source].pop(self.count))))


class Solution(BaseSolution):
    def setup(self) -> None:
        layout_lines, move_lines = self.raw_input.split("\n\n")

        # Stacks
        columns = list(CharacterGrid(layout_lines).iter_columns())
        self.stacks = [
            Stack(("".join(columns[i]))[:-1].strip()) for i in range(1, len(columns), 4)
        ]

        # Moves
        self.moves = []
        for line in move_lines.splitlines():
            _, count, _, source, _, target = line.split()
            self.moves.append(Move(int(source) - 1, int(target) - 1, int(count)))

    def part_1(self) -> str:
        stacks = deepcopy(self.stacks)
        for move in self.moves:
            move.perform(stacks)
        return "".join(stack.peek() for stack in stacks)

    def part_2(self) -> str:
        stacks = deepcopy(self.stacks)
        for move in self.moves:
            move.perform_bulk(stacks)
        return "".join(stack.peek() for stack in stacks)
