import re
from math import prod

from solutions.base import BaseSolution


class Solution(BaseSolution):
    def setup(self) -> None:
        self.games = {}
        for raw_line in self.raw_input.splitlines():
            line = re.sub(r":|;|,", "", raw_line)
            _, raw_game_id, *raw_details = line.split(" ")
            game_id = int(raw_game_id)
            results = {"red": 0, "green": 0, "blue": 0}
            for i in range(0, len(raw_details), 2):
                colour = raw_details[i + 1]
                count = int(raw_details[i])
                results[colour] = max(results[colour], count)
            self.games[game_id] = results

    def part_1(self) -> int:
        max_stones = {"red": 12, "green": 13, "blue": 14}
        valid_games = []
        for game, results in self.games.items():
            for colour, n in results.items():
                if n > max_stones[colour]:
                    break
            else:
                valid_games.append(game)
        return sum(valid_games)

    def part_2(self) -> int:
        return sum(prod(game.values()) for game in self.games.values())
