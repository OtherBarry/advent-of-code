from pathlib import Path
from tempfile import NamedTemporaryFile

from solutions.Y23.day10 import Solution


def test_part_1_easy() -> None:
    with NamedTemporaryFile("w") as f:
        f.write(".....\n.S-7.\n.|.|.\n.L-J.\n.....")
        f.flush()
        solution = Solution(Path(f.name))
    solution.setup()
    assert solution.part_1() == 4


def test_part_1_medium() -> None:
    with NamedTemporaryFile("w") as f:
        f.write("..F7.\n.FJ|.\nSJ.L7\n|F--J\nLJ...")
        f.flush()
        solution = Solution(Path(f.name))
    solution.setup()
    assert solution.part_1() == 8


def test_part_1_hard() -> None:
    with NamedTemporaryFile("w") as f:
        f.write("7-F7-\n.FJ|7\nSJLL7\n|F--J\nLJ.LJ")
        f.flush()
        solution = Solution(Path(f.name))
    solution.setup()
    assert solution.part_1() == 8


def test_part_2_easy() -> None:
    with NamedTemporaryFile("w") as f:
        f.write(
            "...........\n.S-------7.\n.|F-----7|.\n.||.....||.\n.||.....||.\n.|L-7.F-J|.\n.|..|.|..|.\n.L--J.L--J.\n..........."
        )
        f.flush()
        solution = Solution(Path(f.name))
    solution.setup()
    assert solution.part_2() == 4


def test_part_2_medium() -> None:
    with NamedTemporaryFile("w") as f:
        f.write(
            "..........\n.S------7.\n.|F----7|.\n.||....||.\n.||....||.\n.|L-7F-J|.\n.|..||..|.\n.L--JL--J.\n.........."
        )
        f.flush()
        solution = Solution(Path(f.name))
    solution.setup()
    assert solution.part_2() == 4


def test_part_2_hard() -> None:
    with NamedTemporaryFile("w") as f:
        f.write(
            ".F----7F7F7F7F-7....\n.|F--7||||||||FJ....\n.||.FJ||||||||L7....\nFJL7L7LJLJ||LJ.L-7..\nL--J.L7...LJS7F-7L7.\n....F-J..F7FJ|L7L7L7\n....L7.F7||L7|.L7L7|\n.....|FJLJ|FJ|F7|.LJ\n....FJL-7.||.||||...\n....L---J.LJ.LJLJ..."
        )
        f.flush()
        solution = Solution(Path(f.name))
    solution.setup()
    assert solution.part_2() == 8


def test_part_2_extreme() -> None:
    with NamedTemporaryFile("w") as f:
        f.write(
            "FF7FSF7F7F7F7F7F---7\nL|LJ||||||||||||F--J\nFL-7LJLJ||||||LJL-77\nF--JF--7||LJLJ7F7FJ-\nL---JF-JLJ.||-FJLJJ7\n|F|F-JF---7F7-L7L|7|\n|FFJF7L7F-JF7|JL---7\n7-L-JL7||F7|L7F-7F7|\nL.L7LFJ|||||FJL7||LJ\nL7JLJL-JLJLJL--JLJ.L"
        )
        f.flush()
        solution = Solution(Path(f.name))
    solution.setup()
    assert solution.part_2() == 10
