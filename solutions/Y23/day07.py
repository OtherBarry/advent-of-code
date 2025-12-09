from collections import defaultdict
from collections.abc import Iterable
from enum import Enum
from typing import ClassVar

from solutions.base import BaseSolution


class HandType(int, Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    @classmethod
    def from_hand_frequencies(cls, frequencies: list[int]) -> "HandType":  # noqa: PLR0911
        if 5 in frequencies:
            return cls.FIVE_OF_A_KIND
        if 4 in frequencies:
            return cls.FOUR_OF_A_KIND
        if 3 in frequencies and 2 in frequencies:
            return cls.FULL_HOUSE
        if 3 in frequencies:
            return cls.THREE_OF_A_KIND
        if 2 in frequencies:
            if frequencies.count(2) == 2:
                return cls.TWO_PAIR
            return cls.ONE_PAIR
        return cls.HIGH_CARD


class Hand:  # noqa: PLW1641
    CARD_VALUE_MAP: ClassVar = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    def __init__(self, hand: str) -> None:
        self.raw_hand = hand
        self.value_hand = [self.CARD_VALUE_MAP[c] for c in self.raw_hand]
        self.hand = self.list_to_frequency_map(self.value_hand)
        self.hand_type = HandType.from_hand_frequencies(list(self.hand.values()))

    @classmethod
    def list_to_frequency_map(cls, iterable: Iterable[int]) -> dict[int, int]:
        char_frequency_map: dict[int, int] = defaultdict(int)
        for value in iterable:
            char_frequency_map[value] += 1
        return dict(char_frequency_map)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        if self.hand_type == other.hand_type:
            for self_value, other_value in zip(
                self.value_hand, other.value_hand, strict=True
            ):
                if self_value != other_value:
                    return self_value < other_value
        return self.hand_type < other.hand_type

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        return self.hand == other.hand

    def __repr__(self) -> str:
        return f"{self.raw_hand} {self.hand_type.name}"


class Part2Hand(Hand):
    CARD_VALUE_MAP: ClassVar = {
        "A": 13,
        "K": 12,
        "Q": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
        "J": 1,
    }

    @classmethod
    def list_to_frequency_map(cls, iterable: Iterable[int]) -> dict[int, int]:
        char_frequency_map: dict[int, int] = defaultdict(int)
        n_jokers = 0
        for value in iterable:
            if value == cls.CARD_VALUE_MAP["J"]:
                n_jokers += 1
            else:
                char_frequency_map[value] += 1
        try:
            key_with_highest_value = max(
                char_frequency_map, key=char_frequency_map.__getitem__
            )
        except ValueError:
            key_with_highest_value = 1
        char_frequency_map[key_with_highest_value] += n_jokers
        return dict(char_frequency_map)


def calculate_bid_total(sorted_hands: list[tuple[Hand, int]]) -> int:
    total = 0
    for i, (_hand, bid) in enumerate(sorted_hands):
        total += bid * (i + 1)
    return total


class Solution(BaseSolution):
    def generate_hands(self, hand_type: type[Hand]) -> Iterable[tuple[Hand, int]]:
        for line in self.raw_input.splitlines():
            raw_hand, raw_bid = line.split(" ")
            hand = hand_type(raw_hand)
            bid = int(raw_bid)
            yield hand, bid

    def setup(self) -> None:
        pass

    def part_1(self) -> int:
        sorted_hands = sorted(self.generate_hands(Hand), key=lambda x: x[0])
        return calculate_bid_total(sorted_hands)

    def part_2(self) -> int:
        sorted_hands = sorted(self.generate_hands(Part2Hand), key=lambda x: x[0])
        return calculate_bid_total(sorted_hands)
