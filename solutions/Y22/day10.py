from solutions.base import BaseSolution


class Solution(BaseSolution):
    def setup(self) -> None:
        self.x_register = [1]
        for line in self.raw_input.splitlines():
            if line.startswith("addx"):
                _, value = line.split()
                self.x_register.append(self.x_register[-1])
                self.x_register.append(self.x_register[-1] + int(value))
            elif line.startswith("noop"):
                self.x_register.append(self.x_register[-1])
            else:
                raise ValueError(f"Invalid line: {line}")

    def part_1(self) -> int:
        value = 0
        for i in (20, 60, 100, 140, 180, 220):
            value += i * self.x_register[i - 1]
        return value

    def part_2(self) -> str:  # type: ignore[override]
        result = ""
        for index, register in enumerate(self.x_register):
            crt_index = index % 40
            if crt_index == 0:
                result += "\n\t\t"
            if register - 1 <= crt_index <= register + 1:
                result += "█"
            else:
                result += " "
        return result
