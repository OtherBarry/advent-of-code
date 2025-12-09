from typing import Any

from solutions.base import BaseSolution

PRIORITY_MAP = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26,
    "A": 27,
    "B": 28,
    "C": 29,
    "D": 30,
    "E": 31,
    "F": 32,
    "G": 33,
    "H": 34,
    "I": 35,
    "J": 36,
    "K": 37,
    "L": 38,
    "M": 39,
    "N": 40,
    "O": 41,
    "P": 42,
    "Q": 43,
    "R": 44,
    "S": 45,
    "T": 46,
    "U": 47,
    "V": 48,
    "W": 49,
    "X": 50,
    "Y": 51,
    "Z": 52,
}


def chunk_list(list_: list[Any], chunk_size: int) -> list[list[Any]]:
    return [list_[i : i + chunk_size] for i in range(0, len(list_), chunk_size)]


class Solution(BaseSolution):
    def setup(self) -> None:
        self.packs = [
            [PRIORITY_MAP[c] for c in line] for line in self.raw_input.splitlines()
        ]

    def part_1(self) -> int:
        result = 0
        for pack in self.packs:
            midpoint = len(pack) // 2
            intersection = set(pack[:midpoint]) & set(pack[midpoint:])
            result += intersection.pop()
        return result

    def part_2(self) -> int:
        result = 0
        for chunk in chunk_list(self.packs, 3):
            a, b, c = chunk
            intersection = set(a) & set(b) & set(c)
            result += intersection.pop()
        return result
