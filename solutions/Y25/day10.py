import operator
from collections import deque
from dataclasses import dataclass
from functools import cache
from math import gcd
from typing import Iterable, Sequence, Deque, Set, Tuple

from solutions.base import BaseSolution


MAX_LENGTH = 10
BYTES_NEEDED = (MAX_LENGTH + 7) // 8

State = int
Button = int
IndexButton = Iterable[int]

def binary_string_to_int(binary_string: Iterable[str]) -> int:
    return int("".join(binary_string), 2)

def state_from_pattern(pattern: Iterable[str]) -> State:
    return binary_string_to_int("1" if char == "#" else "0" for char in pattern)

def button_from_indices(indices: IndexButton, length: int) -> Button:
    binary_string = ["0"] * length
    for index in indices:
        binary_string[index] = "1"
    return binary_string_to_int(binary_string)

def modifies_state(button: Button, state: State) -> bool:
    return bool(button & state)


@cache
def update_joltage(current_joltage: tuple[int, ...], button: Button) -> tuple[int, ...]:
    length = len(current_joltage)
    return tuple(
        value + 1 if button & (1 << (length - index - 1)) else value
        for index, value in enumerate(current_joltage)
    )





@dataclass
class Machine:
    length: int
    target_state: State
    target_joltage: Sequence[int]
    buttons: Sequence[Button]

    def as_index_button(self, button: Button) -> IndexButton:
        return [
            index
            for index in range(self.length)
            if button & (1 << (self.length - index - 1))
        ]

    @property
    def index_buttons(self) -> Sequence[IndexButton]:
        return [self.as_index_button(button) for button in self.buttons]

    def as_state_string(self, state: State) -> str:
        binary_string = f"{state:0{self.length}b}"
        return "".join("#" if char == "1" else "." for char in binary_string)

    def as_button_string(self, button: Button) -> str:
        return "[" + ",".join(map(str, self.as_index_button(button))) + "]"





    def compute_joltage(self, presses: Iterable[Button]) -> Sequence[int]:
        joltage = tuple([0] * self.length)
        for button in presses:
            joltage = update_joltage(joltage, button)
        return joltage


def bfs_state(target_state: State, buttons: Sequence[Button]) -> Set[Tuple[int, ...]]:
    current_state = 0
    current_presses = []
    to_visit: Deque[State, list[int]] = deque()
    first = True
    visited = {current_state}
    valid_paths = set()

    while first or len(to_visit) > 0:
        first = False
        for button in buttons:
            next_state = current_state ^ button
            if next_state == target_state:
                valid_paths.add(tuple(sorted(current_presses + [button])))
            elif next_state not in visited:
                visited.add(next_state)
                to_visit.append((next_state, current_presses + [button]))
        current_state, current_presses = to_visit.popleft()

    return valid_paths


def bfs_joltage(target_joltage: tuple[int, ...], buttons: Sequence[Button]) -> Sequence[Button] | None:
    current_joltage = tuple([0] * len(target_joltage))
    current_presses = []
    to_visit: Deque[tuple[int, ...], list[Button]] = deque()
    visited = {current_joltage}

    while True:
        if current_joltage == target_joltage or (to_visit and all(not all(x <= y for x, y in zip(next[0], target_joltage)) for next in to_visit)):
            break
        # print("\t\t\tIter")
        for button in buttons:
            next_joltage = update_joltage(current_joltage, button)
            if next_joltage not in visited:
                visited.add(next_joltage)
                to_visit.append((next_joltage, current_presses + [button]))
        current_joltage, current_presses = to_visit.popleft()
    if current_joltage != target_joltage:
        return None
    return current_presses





class Solution(BaseSolution):
    def setup(self) -> None:
        self._machines = []
        for line in self.raw_input.splitlines():
            target_pattern_raw, *buttons_raw, joltage_raw = line.split(" ")
            length = len(target_pattern_raw) - 2
            target_state = state_from_pattern(target_pattern_raw[1:-1])
            buttons = [
                button_from_indices(
                    [int(value) for value in raw_button[1:-1].split(",")],
                    length
                )
                for raw_button in buttons_raw
            ]
            target_joltage = [int(value) for value in joltage_raw[1:-1].split(",")]
            self._machines.append(
                Machine(
                    length=length,
                    target_state=target_state,
                    target_joltage=target_joltage,
                    buttons=buttons
                )
            )


    def part_1(self) -> int:
        total = 0
        for machine in self._machines:
            valid_paths = bfs_state(machine.target_state, machine.buttons)
            total += min(len(path) for path in valid_paths)
        return total

    def part_2(self) -> int:
        total = 0
        for machine in self._machines:
            target_offset_state = state_from_pattern(
                "#" if joltage % 2 == 1 else "."
                for joltage in machine.target_joltage
            )
            offset_presses = bfs_state(target_offset_state, machine.buttons)

            press_counts = []

            print(offset_presses)

            for path in offset_presses:
                # print("Offset press path:", [machine.as_button_string(button) for button in path])

                base_joltage = machine.compute_joltage(path)
                remaining_joltage = tuple(map(operator.sub,
                    machine.target_joltage,
                    base_joltage
                ))
                print("Remaining joltage:", remaining_joltage, gcd(*remaining_joltage))

                multiplier = 1
                while all(value % 2 == 0 for value in remaining_joltage):
                    # print("Halving remaining joltage:", remaining_joltage)
                    remaining_joltage = tuple(value // 2 for value in remaining_joltage)
                    multiplier *= 2

                print("\tReduced joltage:", remaining_joltage)

                even_presses = bfs_joltage(remaining_joltage, tuple(machine.buttons))

                # print(even_presses)

                if even_presses is not None:
                    press_counts.append(len(offset_presses) + (len(even_presses) * multiplier))

            total += min(press_counts)

        return total





        return 0



