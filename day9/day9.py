from typing import List, Tuple, Set
from collections import deque
from pathlib import Path


# assuming that the input file is in the same folder as this script.
def read_input() -> List[str]:
    path_to_input = Path(__file__).parent / "input.txt"
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    return content


def is_within_boundaries(i: int, j: int, rows: int, cols: int) -> bool:
    return i >= 0 and i < rows and j >= 0 and j < cols


# a point is a lowpoint if its height is lower than all of its neighbours
def is_lowpoint(matrix: List[List[int]], i: int, j: int) -> bool:
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # left, up, right, down
    curr_point = matrix[i][j]

    for direction in directions:
        # neighbour coordinate
        r, c = direction[0] + i, direction[1] + j
        if (
            is_within_boundaries(r, c, len(matrix), len(matrix[0]))
            and curr_point >= matrix[r][c]
        ):
            return False

    return True


def find_lowpoints(str_input: List[str]) -> List[Tuple[int, int]]:
    matrix = [[int(col) for col in rows] for rows in str_input]
    low_points = []
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            if is_lowpoint(matrix, i, j):
                low_points.append((i, j))

    return low_points


def get_valid_neighbours(
    matrix: List[List[int]], i: int, j: int, visited: Set[Tuple[int, int]]
) -> List[Tuple[int, int]]:

    """
    The coordinate (i, j) represents the current point we are looking at. 
    (r, c) represents the neighbouring coordinates. 
    """
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # left, up, right, down
    curr_height = matrix[i][j]
    valid_neighbours = []

    for direction in directions:
        # neighbour coordinate
        r, c = direction[0] + i, direction[1] + j
        if (
            is_within_boundaries(r, c, len(matrix), len(matrix[0]))
            and (r, c) not in visited
            and matrix[r][c] != 9
            and matrix[r][c] > curr_height
        ):
            valid_neighbours.append((r, c))

    return valid_neighbours


def bfs(matrix: List[List[int]], low_point: Tuple[int, int]) -> int:
    queue = deque()
    visited = set()
    curr_basin = []

    queue.append(low_point)
    while queue:
        i, j = queue.popleft()
        curr_basin.append((i, j))
        neighbours = get_valid_neighbours(matrix, i, j, visited)

        for neighbour in neighbours:
            visited.add(neighbour)
            queue.append(neighbour)

    return curr_basin


def part_1(content: List[str]) -> int:
    """
    Finding the low points is pretty simple. Just check that every single entry
    in the matrix is less than all its valid neighbours. 
    """
    matrix = [[int(x) for x in numbers] for numbers in content]
    low_points = find_lowpoints(matrix)
    return sum([matrix[p[0]][p[1]] + 1 for p in low_points])


def part_2(content: List[str]) -> int:
    """
    The idea is to:
    1. find all the existing low points. 
    2. perform a bfs from each low point to find the valid nodes that can 
    be included to form the basin for that low point. 
    3. multiply the top 3 largest basins. 
    """

    matrix = [[int(x) for x in numbers] for numbers in content]
    basins = []
    low_points = find_lowpoints(matrix)

    for low_point in low_points:
        basins.append(bfs(matrix, low_point))

    basins.sort(key=lambda x: len(x), reverse=True)

    total = 1
    for basin in basins[:3]:
        total *= len(basin)

    return total


if __name__ == "__main__":
    content = read_input()
    print(f"part 1: {part_1(content)}")
    print(f"part 2: {part_2(content)}")
