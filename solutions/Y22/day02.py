from solutions.base import BaseSolution

PART_1_MOVE_MAP = {
    "A X": "A A",
    "A Y": "A B",
    "A Z": "A C",
    "B X": "B A",
    "B Y": "B B",
    "B Z": "B C",
    "C X": "C A",
    "C Y": "C B",
    "C Z": "C C",
}

PART_2_MOVE_MAP = {
    "A X": "A C",
    "A Y": "A A",
    "A Z": "A B",
    "B X": "B A",
    "B Y": "B B",
    "B Z": "B C",
    "C X": "C B",
    "C Y": "C C",
    "C Z": "C A",
}

SCORE_MAP = {
    "A A": 4,
    "A B": 8,
    "A C": 3,
    "B A": 1,
    "B B": 5,
    "B C": 9,
    "C A": 7,
    "C B": 2,
    "C C": 6,
}


class Solution(BaseSolution):
    def setup(self) -> None:
        self.input = self.raw_input.splitlines()

    def part_1(self) -> int:
        return sum(SCORE_MAP[PART_1_MOVE_MAP[move]] for move in self.input)

    def part_2(self) -> int:
        return sum(SCORE_MAP[PART_2_MOVE_MAP[move]] for move in self.input)
