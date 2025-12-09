from solutions.Y23.day13 import find_reflection, pattern_to_np_array


def test_find_reflection_pattern_a() -> None:
    pattern = (
        "#.##..##.\n..#.##.#.\n##......#\n##......#\n..#.##.#.\n..##..##.\n#.#.##.#."
    )
    array = pattern_to_np_array(pattern)
    assert find_reflection(array) is None
    assert find_reflection(array.T) == 5


def test_find_reflection_pattern_b() -> None:
    pattern = (
        "#...##..#\n#....#..#\n..##..###\n#####.##.\n#####.##.\n..##..###\n#....#..#"
    )
    array = pattern_to_np_array(pattern)
    assert find_reflection(array) == 4
    assert find_reflection(array.T) is None


def test_find_smudgedreflection_pattern_a() -> None:
    pattern = (
        "#.##..##.\n..#.##.#.\n##......#\n##......#\n..#.##.#.\n..##..##.\n#.#.##.#."
    )
    array = pattern_to_np_array(pattern)
    assert find_reflection(array, expected_differences=1) == 3
    assert find_reflection(array.T, expected_differences=1) is None


def test_find_smudged_reflection_pattern_b() -> None:
    pattern = (
        "#...##..#\n#....#..#\n..##..###\n#####.##.\n#####.##.\n..##..###\n#....#..#"
    )
    array = pattern_to_np_array(pattern)
    assert find_reflection(array, expected_differences=1) == 1
    assert find_reflection(array.T, expected_differences=1) is None


def test_find_smudged_reflection_pattern_c() -> None:
    pattern = "#......#....##.\n####.###.#...#.\n####.###.#...#.\n#......#....##.\n..##...#...#...\n..#...#####.#..\n#####.#####.###\n...####...##.#.\n...####...#..#."
    array = pattern_to_np_array(pattern)
    assert find_reflection(array, expected_differences=1) == 8
    assert find_reflection(array.T, expected_differences=1) is None
