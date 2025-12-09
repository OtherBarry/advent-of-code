from heapq import heappop, heappush
from itertools import count
from typing import Optional

import networkx as nx

from solutions.base import BaseSolution
from solutions.utils.grid import Coordinate, Direction, IntegerGrid, manhattan_distance

Node = tuple[int, int, Optional["Direction"], int]


def sum_path(graph: nx.Graph, path: list[Node]) -> int:
    return sum(graph.nodes[node]["weight"] for node in path[1:])


def create_graph(grid: IntegerGrid, min_steps: int, max_steps: int) -> nx.Graph:  # noqa: C901
    graph = nx.DiGraph()
    for coordinate, value in grid.enumerate():
        i, j = coordinate
        neighbours = grid.neighbours(coordinate, include_diagonal=False)
        if i == 0 and j == 0:
            graph.add_node((i, j, None, 0), weight=0)
            for neighbour in neighbours:
                start_direction = Direction.from_coordinates((i, j), neighbour)
                graph.add_edge(
                    (i, j, None, 0), (neighbour[0], neighbour[1], start_direction, 1)
                )
        for direction in Direction:
            for steps in range(1, max_steps + 1):
                graph.add_node((i, j, direction, steps), weight=value)
                for neighbour in neighbours:
                    neighbour_direction = Direction.from_coordinates((i, j), neighbour)
                    if neighbour_direction == -direction:
                        continue
                    if neighbour_direction != direction:
                        if steps >= min_steps:
                            graph.add_edge(
                                (i, j, direction, steps),
                                (neighbour[0], neighbour[1], neighbour_direction, 1),
                            )
                    elif steps < max_steps:
                        graph.add_edge(
                            (i, j, direction, steps),
                            (neighbour[0], neighbour[1], direction, steps + 1),
                        )
    return graph


def astar_path(
    graph: nx.Graph, source_coord: Coordinate, target_coord: Coordinate
) -> list[Node]:
    """
    Determine an optimal path from source to target using the A* algorithm.

    Copied from networkx's A* implementation.

    Modified to:
    - use coordinates as start/end nodes
    - use edge weight property as cost
    - use manhattan distance as heuristic
    """
    source = (source_coord[0], source_coord[1], None, 0)
    adjacency_matrix = graph._adj  # noqa: SLF001
    c = count()
    queue: list[tuple[int, int, tuple[int, int, None, int], int, Node | None]] = [
        (0, next(c), source, 0, None)
    ]
    enqueued: dict[Node, tuple[int, int]] = {}
    explored: dict[Node, Node | None] = {}

    while queue:
        _, __, curnode, dist, parent = heappop(queue)

        i, j, *_ = curnode
        if (i, j) == target_coord:
            path: list[Node] = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if curnode in explored:
            if explored[curnode] is None:
                continue
            qcost, h = enqueued[curnode]
            if qcost < dist:
                continue

        explored[curnode] = parent

        for neighbor in adjacency_matrix[curnode]:
            cost = graph.nodes[neighbor]["weight"]
            ncost = dist + cost
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                if qcost <= ncost:
                    continue
            else:
                h = manhattan_distance(neighbor, target_coord)
            enqueued[neighbor] = ncost, h
            heappush(queue, (ncost + h, next(c), neighbor, ncost, curnode))

    msg = f"Node {target_coord} not reachable from {source_coord}"
    raise nx.NetworkXNoPath(msg)


class Solution(BaseSolution):
    def setup(self) -> None:
        self.grid = IntegerGrid(self.raw_input)

    def part_1(self) -> int:
        graph = create_graph(self.grid, 0, 3)
        path = astar_path(graph, (0, 0), (self.grid.height - 1, self.grid.width - 1))
        return sum_path(graph, path)

    def part_2(self) -> int:
        graph = create_graph(self.grid, 4, 10)
        path = astar_path(graph, (0, 0), (self.grid.height - 1, self.grid.width - 1))
        return sum_path(graph, path)
