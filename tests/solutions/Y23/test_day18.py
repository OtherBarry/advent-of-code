from solutions.utils.grid import Direction
from solutions.Y23.day18 import parse_hex


def test_parse_hex() -> None:
    assert parse_hex("70c710") == (Direction.RIGHT, 461937)
    assert parse_hex("0dc571") == (Direction.DOWN, 56407)
    assert parse_hex("5713f0") == (Direction.RIGHT, 356671)
    assert parse_hex("d2c081") == (Direction.DOWN, 863240)
    assert parse_hex("59c680") == (Direction.RIGHT, 367720)
    assert parse_hex("411b91") == (Direction.DOWN, 266681)
    assert parse_hex("8ceee2") == (Direction.LEFT, 577262)
    assert parse_hex("caa173") == (Direction.UP, 829975)
    assert parse_hex("1b58a2") == (Direction.LEFT, 112010)
    assert parse_hex("caa171") == (Direction.DOWN, 829975)
    assert parse_hex("7807d2") == (Direction.LEFT, 491645)
    assert parse_hex("a77fa3") == (Direction.UP, 686074)
    assert parse_hex("015232") == (Direction.LEFT, 5411)
    assert parse_hex("7a21e3") == (Direction.UP, 500254)
