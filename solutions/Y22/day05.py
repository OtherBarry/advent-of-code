from copy import deepcopy
from dataclasses import dataclass, field

from solutions.base import BaseSolution


def chunk_string(string: str, chunk_size: int) -> list[str]:
    return [string[i : i + chunk_size] for i in range(0, len(string), chunk_size)]


@dataclass
class Stack:
    contents: list[str] = field(default_factory=list)

    def push(self, value: str) -> None:
        self.contents.append(value)

    def pop(self) -> str:
        return self.contents.pop()

    def peek(self) -> str:
        return self.contents[-1]


@dataclass
class Supplies:
    stacks: list[Stack]

    def move_9000(self, source: int, target: int, count: int) -> None:
        for _ in range(count):
            self.stacks[target].push(self.stacks[source].pop())

    def move_9001(self, source: int, target: int, count: int) -> None:
        temp_stack = Stack()
        for _ in range(count):
            temp_stack.push(self.stacks[source].pop())
        for _ in range(count):
            self.stacks[target].push(temp_stack.pop())


class Solution(BaseSolution):
    def setup(self) -> None:
        lines = self.raw_input.splitlines()
        num_stacks = (len(lines[0]) + 1) // 4
        stacks = [Stack() for _ in range(num_stacks)]
        moves_start = -1
        for i, line in enumerate(lines):
            if "[" not in line:
                stacks_end = i
                moves_start = i + 2
                break
        for line in lines[:stacks_end][::-1]:
            for j, chunk in enumerate(chunk_string(line, 4)):
                if chunk != "    ":
                    stacks[j].push(chunk[1])
        self.supplies = Supplies(stacks)
        self.moves = []
        for line in lines[moves_start:]:
            _, count, _, source, _, target = line.split()
            self.moves.append((int(source) - 1, int(target) - 1, int(count)))

    def part_1(self) -> int:
        supplies = deepcopy(self.supplies)
        for move in self.moves:
            supplies.move_9000(*move)
        return int("".join(stack.peek() for stack in supplies.stacks))

    def part_2(self) -> int:
        supplies = deepcopy(self.supplies)
        for move in self.moves:
            supplies.move_9001(*move)
        return int("".join(stack.peek() for stack in supplies.stacks))
