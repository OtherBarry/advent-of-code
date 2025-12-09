from contextlib import suppress

import networkx as nx

from solutions.base import BaseSolution


class Solution(BaseSolution):
    def setup(self) -> None:
        graph = nx.DiGraph()
        start = None
        end = None

        # Add Nodes
        for y, row in enumerate(self.raw_input.splitlines()):
            for x, char in enumerate(row):
                if char == "S":
                    start = (x, y)
                    char = "a"  # noqa: PLW2901
                elif char == "E":
                    end = (x, y)
                    char = "z"  # noqa: PLW2901
                value = ord(char) - ord("a")
                graph.add_node((x, y), char=char, value=value)

        # Add Edges
        for node in graph.nodes:
            x, y = node
            for x_offset, y_offset in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                neighbor = (x + x_offset, y + y_offset)
                if neighbor in graph.nodes:
                    node_value = graph.nodes[node]["value"]
                    neighbor_value = graph.nodes[neighbor]["value"]
                    if neighbor_value - node_value <= 1:
                        graph.add_edge(node, neighbor)

        self.graph = graph
        self.start = start
        self.end = end

    def part_1(self) -> int:
        return nx.shortest_path_length(self.graph, self.start, self.end)

    def part_2(self) -> int:
        a_nodes = [
            node for node in self.graph.nodes if self.graph.nodes[node]["char"] == "a"
        ]
        all_paths = nx.shortest_path_length(self.graph, target=self.end)
        path_lengths = []
        for a_node in a_nodes:
            with suppress(KeyError):
                path_lengths.append(all_paths[a_node])
        return min(path_lengths)
