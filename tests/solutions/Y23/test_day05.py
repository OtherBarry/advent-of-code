from solutions.Y23.day05 import build_map


def test_build_map() -> None:
    range_map = build_map(["50 98 2", "52 50 48"])
    for seed, soil in (
        (98, 50),
        (99, 51),
        (53, 55),
        (10, 10),
        (79, 81),
        (14, 14),
        (55, 57),
        (13, 13),
    ):
        assert range_map.convert_value(seed) == soil


def test_part_1_with_sample_data() -> None:
    """
    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4
    """
    maps = [
        build_map(["50 98 2", "52 50 48"]),  # seed_soil_map
        build_map(["0 15 37", "37 52 2", "39 0 15"]),  # soil_fertilizer_map
        build_map(["49 53 8", "0 11 42", "42 0 7", "57 7 4"]),  # fertilizer_water_map
        build_map(["88 18 7", "18 25 70"]),  # water_light_map
        build_map(["45 77 23", "81 45 19", "68 64 13"]),  # light_temperature_map
        build_map(["0 69 1", "1 0 69"]),  # temperature_humidity_map
        build_map(["60 56 37", "56 93 4"]),  # humidity_location_map
    ]
    for seed, expected in ((79, 82), (14, 43), (55, 86), (13, 35)):
        current = seed
        for range_map in maps:
            current = range_map.convert_value(current)
        assert current == expected
