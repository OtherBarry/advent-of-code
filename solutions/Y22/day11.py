from dataclasses import dataclass, field
from math import lcm
from queue import SimpleQueue

from solutions.base import BaseSolution


@dataclass
class Monkey:
    id: int
    divide: int
    true_target: int
    false_target: int
    items: SimpleQueue[int] = field(default_factory=SimpleQueue)
    multipy: int = 1
    add: int = 0
    factor: int = 1
    inspection_count: int = 0

    @classmethod
    def handle_worry(cls, item: int) -> int:
        return item

    def throw_item(self) -> tuple[int, int]:
        item = self.items.get()
        self.inspection_count += 1
        item = item + self.add
        item = item * self.multipy
        item = item**self.factor
        item = self.handle_worry(item)
        if item % self.divide == 0:
            return item, self.true_target
        return item, self.false_target

    def receive_item(self, item: int) -> None:
        self.items.put(item)

    @classmethod
    def from_string(cls, string: str) -> "Monkey":
        parameters = {}
        lines = string.splitlines()
        id_line = lines[0].replace("Monkey ", "").replace(":", "")
        parameters["id"] = int(id_line)
        operation_line = lines[2].replace("  Operation: new = old ", "")
        operator, value = operation_line.split()
        if operator == "+":
            parameters["add"] = int(value)
        elif operator == "*":
            if value == "old":
                parameters["factor"] = 2
            else:
                parameters["multipy"] = int(value)
        test_line = lines[3].replace("  Test: divisible by ", "")
        parameters["divide"] = int(test_line)
        true_target_line = lines[4].replace("    If true: throw to monkey ", "")
        parameters["true_target"] = int(true_target_line)
        false_target_line = lines[5].replace("    If false: throw to monkey ", "")
        parameters["false_target"] = int(false_target_line)
        monkey = cls(**parameters)  # type: ignore[arg-type]
        items_line = lines[1].replace("  Starting items: ", "")
        for item in items_line.split(", "):
            monkey.receive_item(int(item))
        return monkey


def execute_turn(monkeys: dict[int, Monkey]) -> None:
    for monkey in sorted(monkeys.values(), key=lambda monkey: monkey.id):
        while not monkey.items.empty():
            item, target = monkey.throw_item()
            monkeys[target].receive_item(item)


def calculate_monkey_business(monkeys: dict[int, Monkey]) -> int:
    monkey_list = sorted(
        monkeys.values(), key=lambda monkey: monkey.inspection_count, reverse=True
    )
    return monkey_list[0].inspection_count * monkey_list[1].inspection_count


def generate_monkeys(string: str) -> dict[int, Monkey]:
    monkeys = {}
    for monkey_string in string.split("\n\n"):
        monkey = Monkey.from_string(monkey_string)
        monkeys[monkey.id] = monkey
    return monkeys


class Solution(BaseSolution):
    def setup(self) -> None:
        pass

    def part_1(self) -> int:
        monkeys = generate_monkeys(self.raw_input)
        Monkey.handle_worry = lambda _, item: item // 3  # type: ignore[method-assign, misc, assignment]
        for _ in range(20):
            execute_turn(monkeys)
        return calculate_monkey_business(monkeys)

    def part_2(self) -> int:
        monkeys = generate_monkeys(self.raw_input)
        master_divisor = lcm(*(m.divide for m in monkeys.values()))
        Monkey.handle_worry = lambda _, item: item % master_divisor  # type: ignore[method-assign, misc, assignment]
        for _ in range(10000):
            execute_turn(monkeys)
        return calculate_monkey_business(monkeys)
