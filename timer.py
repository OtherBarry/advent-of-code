from timeit import default_timer
from types import TracebackType
from typing import Self


class Timer:
    def __init__(self) -> None:
        self.start: float | None = None
        self.end: float | None = None

    @staticmethod
    def format_time(time: float) -> str:
        if time < 1:
            return f"{time * 1000:.2f} ms"
        return f"{time:.2f}  s"

    def __enter__(self) -> Self:
        self.start = default_timer()
        return self

    def __exit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.end = default_timer()

    def __str__(self) -> str:
        if self.start is None or self.end is None:
            msg = "Timer has not been run"
            raise ValueError(msg)
        return self.format_time(self.end - self.start)
