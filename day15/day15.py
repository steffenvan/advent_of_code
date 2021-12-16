from typing import List, Tuple, Dict
from pathlib import Path
from collections import defaultdict, deque
import numpy as np

from graph import Graph
from queue import PriorityQueue


def read_input(filename: str) -> List[str]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    content = [[int(num) for num in row] for row in content]
    return content


def within_bounds(grid: List[List[int]], r: int, c: int) -> bool:
    return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[0])


def build_graph(grid: List[List[int]]) -> Graph:
    graph = Graph()
    directions = [[0, -1], [-1, 0], [0, 1], [1, 0]]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for d in directions:
                r = i + d[0]
                c = j + d[1]
                if within_bounds(grid, r, c):
                    graph.add_edge((i, j), (r, c), grid[r][c])
    return graph


def dijsktra(graph: Graph, start: Tuple[int, int], end: Tuple[int, int]) -> int:
    """
    Standard Dijsktra's algorithm implementation. We build up a distance map
    from the start node to all the other nodes in the graph.
    Returns the distance to the from the start node to the specified end node.
    """
    dist_map = {node: float("inf") for node in graph.get_nodes()}
    dist_map[start] = 0
    q = PriorityQueue()
    q.put((0, start))
    
    while not q.empty():
        curr_node_dist, curr_node = q.get()
        neighbours = graph.neighbours(curr_node)
        for neighbour, neighbour_dist in neighbours.items():
            new_dist = curr_node_dist + neighbour_dist
            if new_dist < dist_map[neighbour]:
                dist_map[neighbour] = new_dist
                q.put((new_dist, neighbour))

    return dist_map[end]


def part_1(grid: List[List[int]]) -> int:
    graph = build_graph(grid)
    return dijsktra(graph, (0, 0), (len(grid) - 1, len(grid[0]) - 1))


def update_values(subgrid: List[List[int]]) -> List[List[int]]:
    new_grid = [[0 for _ in range(len(subgrid))] for _ in range(len(subgrid[0]))]
    for i in range(len(subgrid)):
        for j in range(len(subgrid[0])):
            if subgrid[i][j] == 9:
                new_grid[i][j] = 1
            else:
                new_grid[i][j] = subgrid[i][j] + 1

    return new_grid

def build_small_graph(n: int) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    directions = [[0, -1], [-1, 0], [0, 1], [1, 0]]
    small_grid = [[0 for _ in range(5)] for _ in range(5)]
    seen = set()
    seen.add((0, 0))

    graph = defaultdict(list)
    for i in range(n):
        for j in range(n):
            for d in directions:
                r = i + d[0]
                c = j + d[1]
                if within_bounds(small_grid, r, c) and (r, c) not in seen:
                    seen.add((r, c))
                    graph[(i, j)].append((r, c))
    
    return graph


def part_2(grid: List[List[int]], n: int) -> int:
    """
    Overall, we use a level order BFS to generate the new grid. Each of the 
    n * n copies can be seen as a node in a binary tree where the root of this 
    binary tree is (0, 0). 

    First we use numpy.tile to create a (rows * 5, cols * 5) new grid. Each 
    (rows * i, cols * j), for (i, j) in [0, ..., 4] represents a copied subgrid 
    (i.e node) in the new grid.

    Then we build a graph over each (i, j) entry in the smaller (5 x 5) subgrid
    to represent the relation between each copied subgrid, i.e:
    graph = 
            (0, 0) --> (0, 1) --> (0, 2) ... (0, 4)
              |          |          |          ...
             \|/        \|/        \|/
            (1, 0)     (1, 1)     (1, 2)

            ...         ...         ...        ...

            (4, 0) -->  ...   -->   ...      (4, 4)
    
    To update a specific entry in the new grid that has shape 
    (rows * 5, cols * 5), we retrieve the coordinates from the graph, and 
    multiply the coordinates (y, x) with rows and cols. To update the values, 
    we follow the rules specified in the problem description. 

    After we have built the new grid, we can simply use part_1's solution to 
    get the shortest path. 
    """
    rows = len(grid)
    cols = len(grid[0])

    new_grid = np.tile(grid, (n, n))
    graph = build_small_graph(n)
    q = deque()
    mat_q = deque()

    q.append((0, 0))
    mat_q.append(new_grid[: rows, : cols] )

    while q:
        size = len(mat_q)
        for _ in range(size):
            curr = q.popleft()
            sub_grid = mat_q.popleft()

            # get the indices of the new_grid that we wanto update
            y, x = curr[0] * rows, curr[1] * cols 
            new_grid[y : y + rows, x : x + cols] = sub_grid
            incremented_sub_grid = update_values(sub_grid)
            for neighbour in graph[curr]:
                q.append(neighbour)
                mat_q.append(incremented_sub_grid)

    return part_1(new_grid)

if __name__ == "__main__":
    grid = read_input("input.txt")
    print(f"part 1: {part_1(grid)}")
    print(f"part 2: {part_2(grid, 5)}")

