from typing import Deque, List, Set, Tuple
from pathlib import Path
from collections import deque


def read_input(filename: str) -> List[str]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    content = [[int(num) for num in row] for row in content]
    return content


def is_within_bounds(grid: List[List[int]], y: int, x: int):
    return y >= 0 and y < len(grid) and x >= 0 and x < len(grid[0])


def bfs(
    grid: List[List[int]], q: Deque[Tuple[int, int]], exploded: Set[int], flashes: int
) -> List[List[int]]:
    directions = [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1]]

    while q:
        curr = q.popleft()
        flashes += 1
        y, x = curr
        for d in directions:
            y = d[0] + curr[0]
            x = d[1] + curr[1]
            if is_within_bounds(grid, y, x) and (y, x) not in exploded:
                if grid[y][x] == 9:
                    q.append((y, x))
                    grid[y][x] = 0
                    exploded.add((y, x))
                else:
                    grid[y][x] += 1

    return grid, exploded, flashes


def is_all_zeroes(grid: List[List[int]]) -> bool:
    for r in grid:
        for c in r:
            if c != 0:
                return False
    return True


def part_1(grid: List[List[int]], n: int) -> int:
    """
    Overall, we use a BFS to iterate over the neighbours of the entries that
    have a value of 9 before we increment. If an entry's value is 9, we add
    its coordinates to a queue that we will perform the BFS with.
    We maintain a separate grid variable, to keep the "previous" state of the
    grid such that we still know which entries should explode.
    """
    rows = len(grid)
    cols = len(grid[0])
    exploded = set()
    flashes = 0

    for _ in range(n):
        q = deque()
        exploded = set()
        new_grid = grid

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 9:
                    q.append((r, c))
                    exploded.add((r, c))
                    new_grid[r][c] = 0
                elif (r, c) not in exploded:
                    new_grid[r][c] += 1

        new_grid, exploded, flashes = bfs(new_grid, q, exploded, flashes)
        grid = new_grid

    return flashes


def part_2(grid: List[List[int]], n: int) -> int:
    """
    Similary approach as in part_1. Except after each BFS, we check if all the
    values of the grid is 0 and return the iteration at which this happens.
    """
    rows = len(grid)
    cols = len(grid[0])
    exploded = set()
    step = 0

    for i in range(n):
        q = deque()
        exploded = set()
        new_grid = grid
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 9:
                    q.append((r, c))
                    exploded.add((r, c))
                    new_grid[r][c] = 0
                elif (r, c) not in exploded:
                    new_grid[r][c] += 1

        new_grid, exploded, _ = bfs(new_grid, q, exploded, 0)
        grid = new_grid

        if is_all_zeroes(grid):
            step = i + 1
            break

    return step


if __name__ == "__main__":
    content_1 = read_input("input.txt")
    content_2 = read_input("input.txt")
    print(f"part 1: {part_1(content_1, 100)}")
    print(f"part 2: {part_2(content_2, 300)}")
