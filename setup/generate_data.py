import json
from argparse import ArgumentParser
from itertools import count
from pathlib import Path
from time import sleep
from typing import TypedDict

from advent_of_code import solve
from aocd.examples import Example
from aocd.exceptions import PuzzleLockedError
from aocd.models import Puzzle, User


class Answers(TypedDict):
    part_1: str | None
    part_2: str | None


class ExampleData(TypedDict):
    path: str
    answer: Answers


class Day(TypedDict):
    path: str
    answers: Answers
    examples: list[ExampleData]


class AnswerManager:
    def __init__(self, output_path: Path) -> None:
        self._output_path = output_path
        self._answers: dict[int, dict[int, Day]]
        if output_path.exists():
            with output_path.open("r") as f:
                self._answers = json.load(f)
        else:
            self._answers = {}

    def _write_output(self) -> None:
        with self._output_path.open("w") as f:
            json.dump(self._answers, f, indent=4)

    def add_day(self, year: int, day: int, path: str) -> None:
        with Path(path).open("r") as f:
            raw_input = f.read()

        try:
            solution = solve(year, day, 1, raw_input)
            part_1_answer = solution if solution != "0" else None
        except ValueError:
            part_1_answer = None
        try:
            solution = solve(year, day, 2, raw_input)
            part_2_answer = solution if solution != "0" else None
        except ValueError:
            part_2_answer = None

        self._answers.setdefault(year, {})[day] = Day(
            path=path,
            answers=Answers(part_1=part_1_answer, part_2=part_2_answer),
            examples=[],
        )

        self._write_output()

    def add_example(
        self, year: int, day: int, example_path: str, example: Example
    ) -> None:
        example_data = ExampleData(
            path=example_path,
            answer=Answers(part_1=example.answer_a, part_2=example.answer_b),
        )
        self._answers[year][day]["examples"].append(example_data)

        self._write_output()


def write_example(
    folder: Path, day: int, example: Example, index: int | None = None
) -> None:
    example_folder = folder / "examples"
    example_folder.mkdir(parents=True, exist_ok=True)

    if index is None:
        example_path = example_folder / f"{day:02}.txt"
    else:
        example_path = example_folder / f"{day:02}_{index:02}.txt"

    if example_path.exists():
        print(f"\t\tExample data file {example_path} already exists, skipping.")  # noqa: T201
    else:
        with example_path.open("w") as f:
            f.write(example.input_data)


def generate_data(token: str) -> None:
    user = User(token=token)
    answer_manager = AnswerManager(output_path=Path("answers.json"))
    for year in count(start=2015):
        folder = Path(f"inputs/Y{str(year)[2:]}")
        folder.mkdir(parents=True, exist_ok=True)
        for day in range(1, 26):
            print(f"Generating data for Year {year}, Day {day}")  # noqa: T201

            puzzle = Puzzle(year=year, day=day, user=user)

            input_path = folder / f"{day:02}.txt"
            if input_path.exists():
                print(f"\tData file {input_path} already exists, skipping.")  # noqa: T201
                continue

            try:
                with input_path.open("w") as f:
                    f.write(puzzle.input_data)
            except PuzzleLockedError:
                input_path.unlink(missing_ok=True)
                print("\tPuzzle is locked, exiting.")  # noqa: T201
                break

            answer_manager.add_day(year, day, str(input_path))

            print("\tChecking for examples...")  # noqa: T201
            examples = puzzle.examples
            for index, example in enumerate(examples, start=1):
                write_example(folder, day, example, index=index)
                answer_manager.add_example(
                    year,
                    day,
                    str(folder / "examples" / f"{day:02}_{index:02}.txt"),
                    example,
                )

            print("\tFinished, sleeping to avoid rate limiting...")  # noqa: T201
            sleep(1)
        else:
            continue
        if day == 1:
            folder.rmdir()
        break


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--token", type=str, help="Session token for AoC", required=True
    )
    args = parser.parse_args()

    generate_data(args.token)
