import bisect
from multiprocessing import Pool

from solutions.base import BaseSolution


class RangeMap:
    """A map of ranges to values."""

    def __init__(self) -> None:
        self._ranges: list[tuple[int, int, int]] = []
        self._starts: list[int] = []

    def __getitem__(self, item: int) -> int:
        idx = max(0, bisect.bisect(self._starts, item) - 1)
        start, end, value = self._ranges[idx]
        if start <= item <= end:
            return value
        msg = f"Key {item} not found"
        raise KeyError(msg)

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        start, end = key
        range_ = (start, end, value)
        idx = bisect.bisect(self._starts, start)
        self._ranges.insert(idx, range_)
        self._starts.insert(idx, start)

    def __repr__(self) -> str:
        return f"RangeMap({self._ranges})"

    def convert_value(self, value: int) -> int:
        """
        Convert a value using the map.

        :param value: The value to convert
        :return: The converted value
        """
        try:
            return value + self[value]
        except KeyError:
            return value


def build_map(lines: list[str]) -> RangeMap:
    """
    Build a map of seeds to soil.

    :param lines: The lines of the input
    :return: The map of seeds to soil
    """
    range_map = RangeMap()
    for line in lines:
        dest_start, source_start, length = (int(x) for x in line.split(" "))
        source_end = source_start + length - 1
        modifier = dest_start - source_start
        range_map[(source_start, source_end)] = modifier
    return range_map


class Solution(BaseSolution):
    def setup(self) -> None:
        lines = self.raw_input.splitlines()
        self.seeds = [int(s) for s in lines[0].split(" ")[1:]]
        self.maps = [
            build_map(lines[3:26]),  # seed_soil_map
            build_map(lines[28:59]),  # soil_fertilizer_map
            build_map(lines[61:87]),  # fertilizer_water_map
            build_map(lines[89:129]),  # water_light_map
            build_map(lines[131:173]),  # light_temperature_map
            build_map(lines[175:210]),  # temperature_humidity_map
            build_map(lines[212:249]),  # humidity_location_map
        ]

    def seed_to_location(self, seed: int) -> int:
        for range_map in self.maps:
            seed = range_map.convert_value(seed)
        return seed

    def seed_range_to_location(self, range_: tuple[int, int]) -> int:
        start, length = range_
        return min(self.seed_to_location(seed) for seed in range(start, start + length))

    def part_1(self) -> int:
        return min(self.seed_to_location(seed) for seed in self.seeds)

    def part_2(self) -> int:
        seed_ranges = zip(self.seeds[::2], self.seeds[1::2], strict=True)
        with Pool(20) as pool:
            return min(pool.imap(self.seed_range_to_location, seed_ranges))
