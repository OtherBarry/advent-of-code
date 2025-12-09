from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Optional, Self

from solutions.base import BaseSolution


@dataclass
class Node:
    name: str
    is_directory: bool = False
    _size: int = 0
    parent: Self | None = None
    children: list["Node"] = field(default_factory=list)

    @property
    def size(self) -> int:
        return self._size + sum(child.size for child in self.children)

    def add_child(self, child: "Node") -> None:
        self.children.append(child)
        child.parent = self

    def find_child_by_name(self, name: str) -> Optional["Node"]:
        for child in self.children:
            if child.name == name:
                return child
        return None


def find_all_children_matching(
    node: Node, predicate: Callable[[Node], bool]
) -> list[Node]:
    matches = []
    for child in node.children:
        if predicate(child):
            matches.append(child)
        matches.extend(find_all_children_matching(child, predicate))
    return matches


class Solution(BaseSolution):
    def setup(self) -> None:
        root = Node(name="/", is_directory=True)
        current_dir: Node = root
        for line in self.raw_input.splitlines()[1:]:
            if line.startswith("$"):
                line = line[2:]  # noqa: PLW2901
                if line == "ls":
                    continue
                if line == "cd ..":
                    if current_dir.parent is None:
                        raise ValueError("Already at root directory")
                    current_dir = current_dir.parent

                else:
                    child = current_dir.find_child_by_name(line[3:])
                    if child is None:
                        raise ValueError(f"Directory {line[3:]} not found")
                    current_dir = child
            elif line.startswith("dir"):
                line = line[4:]  # noqa: PLW2901
                child = Node(name=line, is_directory=True)
                current_dir.add_child(child)
            else:
                size, name = line.split()
                child = Node(name=name, is_directory=False, _size=int(size))
                current_dir.add_child(child)
        self.root = root

    def part_1(self) -> int:
        def predicate(node: Node) -> bool:
            return node.is_directory and node.size <= 100000

        return sum(
            node.size for node in find_all_children_matching(self.root, predicate)
        )

    def part_2(self) -> int:
        required_size = 70000000 - 30000000
        current_size = self.root.size
        smallest_dir_to_delete = current_size - required_size

        def predicate(node: Node) -> bool:
            return node.is_directory and node.size >= smallest_dir_to_delete

        dirs_to_delete = find_all_children_matching(self.root, predicate)
        smallest = min(dirs_to_delete, key=lambda node: node.size)
        return smallest.size
