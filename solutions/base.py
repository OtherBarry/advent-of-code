from abc import ABC, abstractmethod
from pathlib import Path


class BaseSolution(ABC):
    def __init__(self, input_path: Path) -> None:
        with input_path.open() as f:
            self.raw_input = f.read().rstrip("\n")

    def setup(self) -> None:  # noqa: B027
        pass

    @abstractmethod
    def part_1(self) -> int:
        pass

    @abstractmethod
    def part_2(self) -> int:
        pass
