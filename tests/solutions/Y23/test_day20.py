from solutions.Y23.day20 import Network


def test_simple_network() -> None:
    network = Network.from_lines(
        ["broadcaster -> a, b, c", "%a -> b", "%b -> c", "%c -> inv", "&inv -> a"]
    )
    assert network.push_button() == (8, 4)


def test_simple_network_thousand_x() -> None:
    network = Network.from_lines(
        ["broadcaster -> a, b, c", "%a -> b", "%b -> c", "%c -> inv", "&inv -> a"]
    )
    low_total = 0
    high_total = 0
    for _ in range(1000):
        low, high = network.push_button()
        low_total += low
        high_total += high
    assert low_total == 8000
    assert high_total == 4000
    assert low_total * high_total == 32000000


def test_complex_network() -> None:
    network = Network.from_lines(
        [
            "broadcaster -> a",
            "%a -> inv, con",
            "&inv -> b",
            "%b -> con",
            "&con -> output",
        ]
    )
    assert network.push_button() == (4, 4)
    assert network.push_button() == (4, 2)
    assert network.push_button() == (5, 3)


def test_complex_network_thousand_x() -> None:
    network = Network.from_lines(
        [
            "broadcaster -> a",
            "%a -> inv, con",
            "&inv -> b",
            "%b -> con",
            "&con -> output",
        ]
    )
    low_total = 0
    high_total = 0
    for _ in range(1000):
        low, high = network.push_button()
        low_total += low
        high_total += high
    assert low_total == 4250
    assert high_total == 2750
    assert low_total * high_total == 11687500
