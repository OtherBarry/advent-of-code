from functools import cache

from solutions.base import BaseSolution


@cache
def num_valid_combinations(row: str, groups: tuple[int, ...]) -> int:  # noqa: C901,PLR0911
    """
    Determine the number of valid combinations of springs in a row.

    Basically stolen from https://gist.github.com/Nathan-Fenner/781285b77244f06cf3248a04869e7161
    """
    if len(row) == 0:
        if len(groups) == 0:
            # ran out of row and groups
            return 1
        # ran out of row but not groups
        return 0

    if len(groups) == 0:
        if "#" in row:
            # ran out of groups but there are hashes left
            return 0
        # ran out of groups and there are no hashes left
        return 1

    if len(row) < sum(groups) + (len(groups) - 1):
        # not enough space for the remaining groups
        return 0

    if row[0] == ".":
        return num_valid_combinations(row[1:], groups)

    if row[0] == "#":
        group, *remaining_groups = groups

        if "." in row[:group]:
            # group doesn't fit
            return 0

        try:
            if row[group] == "#":
                # group is too big
                return 0
        except IndexError:
            pass

        # continue with next group
        return num_valid_combinations(row[group + 1 :], tuple(remaining_groups))

    # split into two possibilities
    return num_valid_combinations("#" + row[1:], groups) + num_valid_combinations(
        "." + row[1:], groups
    )


class Solution(BaseSolution):
    def setup(self) -> None:
        self.spring_rows = []
        self.coniguous_groups = []
        for row in self.raw_input.splitlines():
            springs, raw_groups = row.split(" ")
            self.spring_rows.append(springs)
            self.coniguous_groups.append(
                tuple(int(group) for group in raw_groups.split(","))
            )

    def part_1(self) -> int:
        return sum(
            num_valid_combinations(row, groups)
            for row, groups in zip(self.spring_rows, self.coniguous_groups, strict=True)
        )

    def part_2(self) -> int:
        return sum(
            num_valid_combinations("?".join([row] * 5), groups * 5)
            for row, groups in zip(self.spring_rows, self.coniguous_groups, strict=True)
        )
