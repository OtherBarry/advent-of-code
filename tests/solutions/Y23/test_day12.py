import pytest

from solutions.Y23.day12 import num_valid_combinations

# ???.### 1,1,3 - 1 arrangement
# .??..??...?##. 1,1,3 - 4 arrangements
# ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
# ????.#...#... 4,1,1 - 1 arrangement
# ????.######..#####. 1,6,5 - 4 arrangements
# ?###???????? 3,2,1 - 10 arrangements


@pytest.mark.parametrize(
    ("row", "groups", "expected"),
    [
        ("???.###", [1, 1, 3], 1),
        (".??..??...?##.", [1, 1, 3], 4),
        ("?#?#?#?#?#?#?#?", [1, 3, 1, 6], 1),
        ("????.#...#...", [4, 1, 1], 1),
        ("????.######..#####.", [1, 6, 5], 4),
        ("?###????????", [3, 2, 1], 10),
    ],
)
def test_determine_num_possible_combinations(
    row: str, groups: list[int], expected: int
) -> None:
    assert num_valid_combinations(row, tuple(groups)) == expected


def test_multiplication() -> None:
    assert "?".join(["???.###"] * 5) == "???.###????.###????.###????.###????.###"
    assert [1, 1, 3] * 5 == [1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3]
