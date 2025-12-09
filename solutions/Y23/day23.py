import networkx as nx

from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid, Direction, manhattan_distance

SLOPE_DIRECTION_MAP = {
    "<": Direction.LEFT,
    ">": Direction.RIGHT,
    "^": Direction.UP,
    "v": Direction.DOWN,
}


def generate_directed_graph(grid: CharacterGrid) -> nx.DiGraph:
    graph = nx.DiGraph()
    for coordinate, char in grid.enumerate():
        match char:
            case "#":
                continue
            case ".":
                for neighbour in grid.neighbours(coordinate, include_diagonal=False):
                    if grid[neighbour] != "#":
                        graph.add_edge(coordinate, neighbour)
            case _:
                graph.add_edge(coordinate, SLOPE_DIRECTION_MAP[char].apply(coordinate))

    return graph


def generated_undirected_graph(grid: CharacterGrid) -> nx.Graph:
    graph = nx.grid_2d_graph(grid.height, grid.width)
    for coordinate, char in grid.enumerate():
        if char == "#":
            graph.remove_node(coordinate)
    return graph


def prune_graph(graph: nx.Graph) -> nx.Graph:
    """Prune a graph by removing nodes with only two neighbours, and connecting the neighbours."""
    nx.set_edge_attributes(graph, 1, "weight")

    def is_node_to_prune(node: tuple[int, int]) -> bool:
        return len(graph[node]) == 2

    def prune_node(node: tuple[int, int]) -> None:
        neighbours = list(graph[node])
        new_weight = (
            graph.edges[neighbours[0], node]["weight"]
            + graph.edges[neighbours[1], node]["weight"]
        )
        graph.remove_node(node)
        graph.add_edge(*neighbours, weight=new_weight)

    nodes_to_prune = [node for node in graph if is_node_to_prune(node)]
    while nodes_to_prune:
        for node in nodes_to_prune:
            prune_node(node)
        nodes_to_prune = [node for node in graph if is_node_to_prune(node)]
    return graph


def path_length(path: list[tuple[int, int]]) -> int:
    return sum(manhattan_distance(path[i - 1], path[i]) for i in range(1, len(path)))


class Solution(BaseSolution):
    def setup(self) -> None:
        self.grid = CharacterGrid(self.raw_input)
        self.start = (0, 1)
        self.end = (self.grid.height - 1, self.grid.width - 2)

    def part_1(self) -> int:
        graph = generate_directed_graph(self.grid)
        paths = nx.all_simple_paths(graph, self.start, self.end)
        return max(len(path) for path in paths) - 1

    def part_2(self) -> int:
        graph = generated_undirected_graph(self.grid)
        graph = prune_graph(graph)
        paths = nx.all_simple_paths(graph, self.start, self.end)
        return max(nx.path_weight(graph, path, "weight") for path in paths)
