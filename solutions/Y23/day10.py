import networkx as nx

from solutions.base import BaseSolution
from solutions.utils.grid import CharacterGrid, Coordinate, Direction


def coordinate_in_bounds(
    coordinate: Coordinate, y_max: int, x_max: int, y_min: int, x_min: int
) -> bool:
    """
    Check if a coordinate is in bounds of the given lines.

    :param coordinate: The coordinate to check.
    :param y_min: The minimum y value.
    :param y_max: The maximum y value.
    :param x_min: The minimum x value.
    :param x_max: The maximum x value.
    :returns: True if the coordinate is in bounds, False otherwise.
    """
    y, x = coordinate
    return y_min <= y < y_max and x_min <= x < x_max


def generate_valid_connections(node: Coordinate, pipe_type: str) -> list[Coordinate]:  # noqa: PLR0911
    """
    Generate the valid connections for a node.

    :param node: The node to generate connections for.
    :param pipe_type: The type of pipe at the node.
    :returns: A list of valid connections.
    """
    if pipe_type == "|":
        return [Direction.UP.apply(node), Direction.DOWN.apply(node)]
    if pipe_type == "-":
        return [Direction.RIGHT.apply(node), Direction.LEFT.apply(node)]
    if pipe_type == "L":
        return [Direction.UP.apply(node), Direction.RIGHT.apply(node)]
    if pipe_type == "J":
        return [Direction.UP.apply(node), Direction.LEFT.apply(node)]
    if pipe_type == "7":
        return [Direction.DOWN.apply(node), Direction.LEFT.apply(node)]
    if pipe_type == "F":
        return [Direction.DOWN.apply(node), Direction.RIGHT.apply(node)]
    if pipe_type == "S":
        return [
            Direction.UP.apply(node),
            Direction.DOWN.apply(node),
            Direction.RIGHT.apply(node),
            Direction.LEFT.apply(node),
        ]
    return []


def node_is_even(node: Coordinate) -> bool:
    """
    Check if all coords of a node are even.

    :param node: The node to check.
    :returns: True if the node is even, False otherwise.
    """
    y, x = node
    return y % 2 == 0 and x % 2 == 0


class Solution(BaseSolution):
    def setup(self) -> None:
        self.grid = CharacterGrid(self.raw_input)
        self.start_node = None

        all_pipes = nx.Graph()
        for node, value in self.grid.enumerate():
            if value == ".":
                continue
            if value == "S":
                self.start_node = node
                continue
            for con in generate_valid_connections(node, value):
                if con in self.grid:
                    connections_connections = generate_valid_connections(
                        con, self.grid[con]
                    )
                    if node in connections_connections:
                        all_pipes.add_edge(node, con)
        self.main_loop_graph = nx.bfs_tree(all_pipes, self.start_node)

        self.ground_graph = nx.grid_2d_graph(self.grid.height * 2, self.grid.width * 2)
        for node in self.main_loop_graph.nodes:
            external_node = (node[0] * 2, node[1] * 2)
            self.ground_graph.remove_node(external_node)
            for con in generate_valid_connections(external_node, self.grid[node]):
                if con in self.ground_graph:
                    self.ground_graph.remove_node(con)

    def part_1(self) -> int:
        paths: dict[Coordinate, int] = nx.shortest_path_length(
            self.main_loop_graph, self.start_node
        )
        return max(paths.values())

    def part_2(self) -> int:
        total_contained = 0
        for component in nx.connected_components(self.ground_graph):
            if all(
                coordinate_in_bounds(
                    n,
                    (self.grid.height * 2) - 1,
                    (self.grid.width * 2) - 1,
                    y_min=1,
                    x_min=1,
                )
                for n in component
            ):
                total_contained += sum(1 for n in component if node_is_even(n))
        return total_contained
