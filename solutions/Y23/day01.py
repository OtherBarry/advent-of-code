from typing import ClassVar

from solutions.base import BaseSolution


class Solution(BaseSolution):
    DICT_TRIE: ClassVar = {
        "o": {"n": {"e": "1"}},
        "t": {"w": {"o": "2"}, "h": {"r": {"e": {"e": "3"}}}},
        "f": {"o": {"u": {"r": "4"}}, "i": {"v": {"e": "5"}}},
        "s": {"i": {"x": "6"}, "e": {"v": {"e": {"n": "7"}}}},
        "e": {"i": {"g": {"h": {"t": "8"}}}},
        "n": {"i": {"n": {"e": "9"}}},
    }

    @classmethod
    def extract_digit(cls, line: str, reverse: bool = False) -> str:
        """
        Extract the first (or last) digit from a string.

        :param line: The string to extract the digit from
        :param reverse: Whether to extract the last digit instead of the first
        :return: The first (or last) digit in the string
        """
        range_ = range(len(line) - 1, -1, -1) if reverse else range(len(line))
        for i in range_:
            if line[i].isdigit():
                return line[i]
        msg = "No digit found"
        raise ValueError(msg)

    @classmethod
    def extract_digit_with_words(cls, line: str, reverse: bool = False) -> str:
        """
        Extract the first (or last) digit from a string.

        Includes digits as words (e.g. "one" -> "1").

        :param line: The string to extract the digit from
        :param reverse: Whether to extract the last digit instead of the first
        :return: The first (or last) digit in the string
        """
        range_ = range(len(line) - 1, -1, -1) if reverse else range(len(line))
        for i in range_:
            if line[i].isdigit():
                return line[i]
            n = 0
            node = cls.DICT_TRIE
            while True:
                try:
                    node = node[line[i + n]]  # type: ignore[assignment]
                except (KeyError, IndexError):
                    break
                else:
                    if isinstance(node, str):  # type: ignore[unreachable]
                        return node  # type: ignore[unreachable]
                n += 1

        msg = "No digit found"
        raise ValueError(msg)

    @classmethod
    def calculate_calibration_value(cls, line: str, include_words: bool) -> int:
        """
        Calculate the calibration value of a string.

        :param line: The string to calculate the calibration value of
        :param include_words: Whether to allow digits as words (e.g. "one" -> "1")
        :return: The calibration value of the string
        """
        func = cls.extract_digit_with_words if include_words else cls.extract_digit
        first = func(line)
        last = func(line, reverse=True)
        return int(first + last)

    def setup(self) -> None:
        self.lines = self.raw_input.splitlines()

    def part_1(self) -> int:
        return sum(
            self.calculate_calibration_value(line, include_words=False)
            for line in self.lines
        )

    def part_2(self) -> int:
        return sum(
            self.calculate_calibration_value(line, include_words=True)
            for line in self.lines
        )
