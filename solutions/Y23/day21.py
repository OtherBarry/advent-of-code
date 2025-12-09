from collections.abc import Iterator
from queue import Queue

import networkx as nx

from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid, Coordinate


def dfs_nodes_of_depth(
    graph: nx.Graph, start: Coordinate, depth: int
) -> Iterator[Coordinate]:
    returned = set()
    queue: Queue[tuple[Coordinate, int]] = Queue()
    queue.put((start, 0))
    depth_evenness = depth % 2
    backtrack_threshold = depth - 1
    while not queue.empty():
        node, node_depth = queue.get()
        if node in returned:
            continue
        if node_depth == depth:
            yield node
            returned.add(node)
        else:
            if node_depth % 2 == depth_evenness and node_depth < backtrack_threshold:
                yield node
                returned.add(node)
            for neighbour in graph.neighbors(node):
                queue.put((neighbour, node_depth + 1))


class Solution(BaseSolution):
    def setup(self) -> None:
        self.grid = CharacterGrid(self.raw_input)
        self.graph = nx.grid_2d_graph(self.grid.height, self.grid.width)
        self.start = (-1, -1)
        for coordinate, cell in self.grid.enumerate():
            if cell == "#":
                self.graph.remove_node(coordinate)
            elif cell == "S":
                self.start = coordinate

    def part_1(self) -> int:
        return sum(1 for _ in dfs_nodes_of_depth(self.graph, self.start, 64))

    def part_2(self) -> int:
        return -1
