from solutions.base import BaseSolution


class Page:  # noqa: PLW1641
    def __init__(self, page_number: int) -> None:
        self.page_number = page_number
        self._must_come_before = set[int]()

    def must_come_before(self, page_number: int) -> None:
        self._must_come_before.add(page_number)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Page):
            return NotImplemented
        return other.page_number in self._must_come_before

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Page):
            return NotImplemented
        return self.page_number == other.page_number


def get_middle_page_number(pages: list[Page]) -> int:
    return pages[len(pages) // 2].page_number


class Solution(BaseSolution):
    def setup(self) -> None:
        # Parse input (normal setup)
        raw_rules, raw_updates = self.raw_input.split("\n\n")
        pages = dict[int, Page]()
        for rule_line in raw_rules.splitlines():
            page, before = rule_line.split("|")
            pages.setdefault(int(page), Page(int(page))).must_come_before(int(before))
        self.updates = [
            [pages[int(page)] for page in update.split(",")]
            for update in raw_updates.splitlines()
        ]

        # Run logic in setup because it's easier to do both parts at once
        self._part_1_result = 0
        self._part_2_result = 0

        for update in self.updates:
            sorted_update = sorted(update)
            if sorted_update == update:
                self._part_1_result += get_middle_page_number(update)
            else:
                self._part_2_result += get_middle_page_number(sorted_update)

    def part_1(self) -> int:
        return self._part_1_result

    def part_2(self) -> int:
        return self._part_2_result
