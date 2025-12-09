import numpy as np
import pytest

from solutions.Y23.day14 import Mirror, tilt_row


@pytest.mark.parametrize(
    ("raw_row", "expected"),
    [
        ("OO.O.O..##", "OOOO....##"),
        ("...OO....O", "OOO......."),
        (".O...#O..O", "O....#OO.."),
        (".O.#......", "O..#......"),
        (".#.O......", ".#O......."),
        ("#.#..O#.##", "#.#O..#.##"),
        ("..#...O.#.", "..#O....#."),
        ("....O#.O#.", "O....#O.#."),
        ("....#.....", "....#....."),
        (".#.O.#O...", ".#O..#O..."),
    ],
)
def test_tilt_row(raw_row: str, expected: str) -> None:
    row = np.array(list(raw_row))
    tilt_row(row)  # type: ignore[arg-type]
    assert "".join(row) == expected


def test_mirror_serialisation() -> None:
    raw_mirror = "O....#....\nO.OO#....#\n.....##...\nOO.#O....O\n.O.....O#.\nO.#..O.#.#\n..O..#O..O\n.......O..\n#....###..\n#OO..#...."
    assert str(Mirror.from_str(raw_mirror).normal_form()) == raw_mirror


def test_mirror_rotate() -> None:
    raw_mirror = "O....#....\nO.OO#....#\n.....##...\nOO.#O....O\n.O.....O#.\nO.#..O.#.#\n..O..#O..O\n.......O..\n#....###..\n#OO..#...."
    expected = "OOOO.#.O..\nOO..#....#\nOO..O##..O\nO..#.OO...\n........#.\n..#....#.#\n..O..#.O.O\n..O.......\n#....###..\n#....#...."
    rotated = Mirror.from_str(raw_mirror).tilt()
    assert rotated.calculate_load() == 136
    assert str(rotated.normal_form()) == expected


def test_mirror_cycle_single() -> None:
    raw_mirror = "O....#....\nO.OO#....#\n.....##...\nOO.#O....O\n.O.....O#.\nO.#..O.#.#\n..O..#O..O\n.......O..\n#....###..\n#OO..#...."
    expected = ".....#....\n....#...O#\n...OO##...\n.OO#......\n.....OOO#.\n.O#...O#.#\n....O#....\n......OOOO\n#...O###..\n#..OO#...."
    mirror = Mirror.from_str(raw_mirror)
    mirror.cycle()
    assert str(mirror.normal_form()) == expected


def test_mirror_cycle_double() -> None:
    raw_mirror = "O....#....\nO.OO#....#\n.....##...\nOO.#O....O\n.O.....O#.\nO.#..O.#.#\n..O..#O..O\n.......O..\n#....###..\n#OO..#...."
    expected = ".....#....\n....#...O#\n.....##...\n..O#......\n.....OOO#.\n.O#...O#.#\n....O#...O\n.......OOO\n#..OO###..\n#.OOO#...O"
    mirror = Mirror.from_str(raw_mirror)
    mirror.cycle().cycle()
    assert str(mirror.normal_form()) == expected


def test_mirror_cycle_triple() -> None:
    raw_mirror = "O....#....\nO.OO#....#\n.....##...\nOO.#O....O\n.O.....O#.\nO.#..O.#.#\n..O..#O..O\n.......O..\n#....###..\n#OO..#...."
    expected = ".....#....\n....#...O#\n.....##...\n..O#......\n.....OOO#.\n.O#...O#.#\n....O#...O\n.......OOO\n#...O###.O\n#.OOO#...O"
    mirror = Mirror.from_str(raw_mirror)
    mirror.cycle().cycle().cycle()
    assert str(mirror.normal_form()) == expected


def test_run_cycles() -> None:
    raw_mirror = "O....#....\nO.OO#....#\n.....##...\nOO.#O....O\n.O.....O#.\nO.#..O.#.#\n..O..#O..O\n.......O..\n#....###..\n#OO..#...."
    mirror = Mirror.from_str(raw_mirror)
    assert mirror.run_cycles(1_000_000_000).rotate().calculate_load() == 64
