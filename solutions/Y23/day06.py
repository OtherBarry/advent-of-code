from solutions.base import BaseSolution


def get_n_winning_times(time: int, distance: int) -> int:
    winning_times = 0
    for hold_time in range(time):
        remaining_time = time - hold_time
        achieved_distance = remaining_time * hold_time
        if achieved_distance > distance:
            winning_times += 1
    return winning_times


class Solution(BaseSolution):
    def setup(self) -> None:
        lines = self.raw_input.splitlines()
        self.time_line = lines[0]
        self.distance_line = lines[1]

    def part_1(self) -> int:
        times = [int(t) for t in self.time_line.split(" ")[1:] if t]
        distances = [int(d) for d in self.distance_line.split(" ")[1:] if d]
        total_result = 1
        for i, time in enumerate(times):
            required_distance = distances[i]
            total_result *= get_n_winning_times(time, required_distance)
        return total_result

    def part_2(self) -> int:
        time = int(self.time_line.replace(" ", "").split(":")[1])
        distance = int(self.distance_line.replace(" ", "").split(":")[1])
        return get_n_winning_times(time, distance)
