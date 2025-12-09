import pytest

from solutions.Y23.day07 import Hand, HandType, Part2Hand, calculate_bid_total


@pytest.mark.parametrize(
    ("hand", "hand_type"),
    [
        ("32T3K", HandType.ONE_PAIR),
        ("KK677", HandType.TWO_PAIR),
        ("KTJJT", HandType.TWO_PAIR),
        ("T55J5", HandType.THREE_OF_A_KIND),
        ("QQQJA", HandType.THREE_OF_A_KIND),
    ],
)
def test_hand_types(hand: str, hand_type: HandType) -> None:
    assert Hand(hand).hand_type == hand_type


def test_hand_ranking() -> None:
    hands = ["32T3K", "T55J5", "KK677", "KTJJT", "QQQJA"]
    sorted_hands = sorted(hands, key=lambda x: Hand(x))
    assert sorted_hands == ["32T3K", "KTJJT", "KK677", "T55J5", "QQQJA"]


def test_calculate_bid_total() -> None:
    sorted_hands = [
        (Hand("32T3K"), 765),
        (Hand("KTJJT"), 220),
        (Hand("KK677"), 28),
        (Hand("T55J5"), 684),
        (Hand("QQQJA"), 483),
    ]
    assert calculate_bid_total(sorted_hands) == 6440


@pytest.mark.parametrize(
    ("hand", "hand_type"),
    [
        ("32T3K", HandType.ONE_PAIR),
        ("KK677", HandType.TWO_PAIR),
        ("KTJJT", HandType.FOUR_OF_A_KIND),
        ("T55J5", HandType.FOUR_OF_A_KIND),
        ("QQQJA", HandType.FOUR_OF_A_KIND),
    ],
)
def test_part_2_hand_types(hand: str, hand_type: HandType) -> None:
    assert Part2Hand(hand).hand_type == hand_type
