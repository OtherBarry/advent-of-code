from collections.abc import Callable, Generator
from dataclasses import dataclass, field
from functools import cached_property

from solutions.base import BaseSolution


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    parent: "Directory | None" = None
    files: list[File] = field(default_factory=list)
    subdirectories: list["Directory"] = field(default_factory=list)

    @cached_property
    def size(self) -> int:
        return sum(x.size for x in self.files + self.subdirectories)

    def parse_ls_output(self, line: str) -> None:
        if line.startswith("dir"):
            path = line[4:].strip()
            self.subdirectories.append(Directory(name=path, parent=self))
        else:
            size, name = line.split()
            self.files.append(File(name=name, size=int(size)))


class Shell:
    def __init__(self) -> None:
        self._root = Directory(name="/")
        self._cwd = self._root

    @property
    def root(self) -> Directory:
        return self._root

    def cd(self, path: str) -> None:
        if path == "/":
            self._cwd = self._root
        elif path == "..":
            if self._cwd.parent is None:
                raise ValueError("Already at root directory")
            self._cwd = self._cwd.parent
        else:
            for subdir in self._cwd.subdirectories:
                if subdir.name == path:
                    self._cwd = subdir
                    break
            else:
                raise ValueError(f"Directory {path} not found")

    def parse_line(self, line: str) -> None:
        if line.startswith("$ cd"):
            path = line[5:].strip()
            self.cd(path)
        elif not line.startswith("$ ls"):
            self._cwd.parse_ls_output(line)


def filter_child_directories(
    directory: Directory, predicate: Callable[[Directory], bool]
) -> Generator[Directory]:
    if predicate(directory):
        yield directory
    for subdirectory in directory.subdirectories:
        yield from filter_child_directories(subdirectory, predicate)


class Solution(BaseSolution):
    def setup(self) -> None:
        self._shell = Shell()
        for line in self.raw_input.splitlines():
            self._shell.parse_line(line)

    def part_1(self) -> int:
        def predicate(directory: Directory) -> bool:
            return directory.size <= 100000

        return sum(
            directory.size
            for directory in filter_child_directories(self._shell.root, predicate)
        )

    def part_2(self) -> int:
        required_size = 70000000 - 30000000
        current_size = self._shell.root.size
        minimum_size = current_size - required_size

        def predicate(directory: Directory) -> bool:
            return directory.size >= minimum_size

        return min(
            filter_child_directories(self._shell.root, predicate),
            key=lambda directory: directory.size,
        ).size
