from solutions.base import BaseSolution


class Solution(BaseSolution):
    def setup(self) -> None:
        self._start_position = 50
        self._movements = []
        for line in self.raw_input.splitlines():
            direction = -1 if line[0] == "L" else 1
            distance = int(line[1:])
            self._movements.append(direction * distance)

    def part_1(self) -> int:
        zero_count = 0
        position = self._start_position
        for movement in self._movements:
            position = (position + movement) % 100
            if position == 0:
                zero_count += 1
        return zero_count

    def part_2(self) -> int:
        # TODO: There should be a mathematical way to do this without simulating every step
        zero_count = 0
        position = self._start_position
        for movement in self._movements:
            click_step = 1 if movement >= 0 else -1
            for _ in range(abs(movement)):
                position = (position + click_step) % 100
                if position == 0:
                    zero_count += 1
        return zero_count
