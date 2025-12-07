import argparse
import json
from pathlib import Path

from solutions.base import BaseSolution
from timer import Timer
from utils import get_default_input_path, get_solution_class


def compare_answers(actual: str | int, expected: str | None) -> str:
    if expected is None:
        return "❓"
    if isinstance(actual, int):
        try:
            int_expected = int(expected)
        except ValueError:
            pass
        else:
            if int_expected != actual:
                return "❌" + (" (too low)" if int_expected > actual else " (too high)")
    return "✅" if str(actual) == expected else "❌"


def run(
    solution: BaseSolution, p1_expected: str | None, p2_expected: str | None
) -> None:
    with Timer() as timer:
        solution.setup()
    print(f"\tSetup run in {timer}")  # noqa: T201
    with Timer() as timer:
        p1_result = solution.part_1()
    print(  # noqa: T201
        f"\tPart 1 ({timer}): {p1_result}    {compare_answers(p1_result, p1_expected)}"
    )
    with Timer() as timer:
        p2_result = solution.part_2()
    print(  # noqa: T201
        f"\tPart 2 ({timer}): {p2_result}    {compare_answers(p2_result, p2_expected)}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, help="The year of the problems to run")
    parser.add_argument("problems", nargs="*", type=int, help="The problems to run")
    parser.add_argument(
        "--example", action="store_true", help="Use example input files"
    )
    args = parser.parse_args()
    print("Running problems")  # noqa: T201

    with Path("answers.json").open("r") as f:
        answers = json.load(f)

    with Timer() as timer:
        for problem in args.problems:
            print(f"\nProblem {problem}:")  # noqa: T201

            solution_class = get_solution_class(args.year, problem)

            if args.example:
                for index, example in enumerate(
                    answers.get(str(args.year), {})
                    .get(str(problem), {})
                    .get("examples", [])
                ):
                    print(f"\tExample {index + 1}:")  # noqa: T201
                    path = Path(example["path"])
                    answer_data = example.get("answer", {})
                    solution = solution_class(path)
                    run(solution, answer_data.get("part_1"), answer_data.get("part_2"))

            else:
                answer_data = (
                    answers.get(str(args.year), {})
                    .get(str(problem), {})
                    .get("answers", {})
                )
                input_path = get_default_input_path(args.year, problem)
                solution = solution_class(input_path)
                run(solution, answer_data.get("part_1"), answer_data.get("part_2"))
    print(f"\nTotal time: {timer}")  # noqa: T201
