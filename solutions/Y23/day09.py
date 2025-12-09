from solutions.base import BaseSolution


def calculate_difference(history: list[int]) -> list[int]:
    return [history[i] - history[i - 1] for i in range(1, len(history))]


def predict_next_value(history: list[int]) -> int:
    if any(history):
        return history[-1] + predict_next_value(calculate_difference(history))
    return 0


def predict_previous_value(history: list[int]) -> int:
    if any(history):
        return history[0] - predict_previous_value(calculate_difference(history))
    return 0


class Solution(BaseSolution):
    def setup(self) -> None:
        self.histories = [
            [int(x) for x in line.split(" ")] for line in self.raw_input.splitlines()
        ]

    def part_1(self) -> int:
        return sum(predict_next_value(history) for history in self.histories)

    def part_2(self) -> int:
        return sum(predict_previous_value(history) for history in self.histories)
