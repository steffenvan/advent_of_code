from collections import defaultdict
from typing import Dict, Tuple, Set


class Graph:
    """
    The Graph implementation that we use for this problem. Internally, we
    represent the graph as a nested dictionary, where the each node: Tuple
    maps to a dictionary that represents its neighbours and the weights of
    the edge to them.
    Example: imagine the input is:

    12
    34

    Then the graph will be:
    graph = {
        (0, 0): {
            (0, 1): 2,
            (1, 0): 3
        },
        (0, 1): {
            (0, 0): 1,
            (1, 1): 4
        },
        (1, 0): {
            (0, 0): 1,
            (1, 1): 4
        },
        (1, 1): {
            (0, 1): 2,
            (1, 0): 3
        }
    }
    """

    def __init__(self):
        self.graph = defaultdict(defaultdict)

    def add_edge(self, source, dest, weight):
        self.graph[source][dest] = weight

    def get_nodes(self) -> Set[Tuple[int, int]]:
        return set(self.graph.keys())

    def neighbours(self, node: Tuple[int, int]) -> Dict[Tuple[int, int], int]:
        return self.graph[node]

    def all_vertices(self):
        return set(self.graph.keys())

    def num_vertices(self) -> int:
        return len(self.graph)
