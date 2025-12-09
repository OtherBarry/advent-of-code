import pytest

from solutions.Y24.day02 import check_report, check_report_with_dampener


@pytest.mark.parametrize(
    ("report", "safe"),
    [
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], False),
        ([8, 6, 4, 4, 1], False),
        ([1, 3, 6, 7, 9], True),
    ],
)
def test_check_report(report: list[int], safe: bool) -> None:
    assert check_report(report) == safe


@pytest.mark.parametrize(
    ("report", "safe"),
    [
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], True),
        ([8, 6, 4, 4, 1], True),
        ([1, 3, 6, 7, 9], True),
    ],
)
def test_report_level_with_dampener(report: list[int], safe: bool) -> None:
    assert check_report_with_dampener(report) == safe
