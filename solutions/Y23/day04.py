from solutions.base import BaseSolution


class Solution(BaseSolution):
    def setup(self) -> None:
        self.cards = []
        for line in self.raw_input.splitlines():
            winners = {int(line[i : i + 2]) for i in range(10, 40, 3)}
            values = {int(line[i : i + 2]) for i in range(42, 116, 3)}
            self.cards.append(len(winners & values))

    def part_1(self) -> int:
        winner_points = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        return sum(map(winner_points.__getitem__, self.cards))

    def part_2(self) -> int:
        count = [0] * len(self.cards)
        for i in range(len(self.cards)):
            count[i] += 1
            for j in range(i + 1, i + 1 + self.cards[i]):
                count[j] += count[i]
        return sum(count)
