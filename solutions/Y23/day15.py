import contextlib
from collections import defaultdict

from solutions.base import BaseSolution


def ascii_hash(string: str) -> int:
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value


class Solution(BaseSolution):
    def setup(self) -> None:
        self.sequences = self.raw_input.replace("\n", "").split(",")

    def part_1(self) -> int:
        return sum(ascii_hash(s) for s in self.sequences)

    def part_2(self) -> int:
        boxes: dict[int, dict[str, int]] = defaultdict(dict)

        for sequence in self.sequences:
            if sequence[-1] == "-":
                lens_label = sequence[:-1]
                box_number = ascii_hash(lens_label)
                with contextlib.suppress(KeyError):
                    del boxes[box_number][lens_label]
            else:
                lens_label, focal_length = sequence.split("=")
                box_number = ascii_hash(lens_label)
                boxes[box_number][lens_label] = int(focal_length)

        focal_power = 0
        for box_number, lenses in boxes.items():
            for lens_number, lens_focal_length in enumerate(lenses.values()):
                focal_power += (box_number + 1) * (lens_number + 1) * lens_focal_length

        return focal_power
