from solutions.base import BaseSolution


class MaxLengthStack:
    # TODO: Optimise unique-ness check
    def __init__(self, max_length: int = 4) -> None:
        self.max_length = max_length
        self._stack: list[str] = []

    def push(self, value: str) -> None:
        if len(self._stack) == self.max_length:
            self._stack.pop(0)
        self._stack.append(value)

    def is_unique(self) -> bool:
        return len(self._stack) == self.max_length and len(set(self._stack)) == len(
            self._stack
        )


class Solution(BaseSolution):
    def setup(self) -> None:
        pass

    def part_1(self) -> int:
        stack = MaxLengthStack(4)
        for i, v in enumerate(self.raw_input):
            stack.push(v)
            if stack.is_unique():
                return i + 1
        raise ValueError("No unique sequence found")

    def part_2(self) -> int:
        stack = MaxLengthStack(14)
        for i, v in enumerate(self.raw_input):
            stack.push(v)
            if stack.is_unique():
                return i + 1
        raise ValueError("No unique sequence found")
