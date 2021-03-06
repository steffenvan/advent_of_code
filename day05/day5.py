from typing import List, Tuple
from pathlib import Path
from point import Point


def get_list_of_points(content: List[str]) -> List[List[Point]]:
    """
    Creating a list of pairs: (from: Point, to: Point) objects.
    """
    all_pairs = [pair.split(" -> ") for pair in content]
    return [[Point(point.split(",")) for point in pairs] for pairs in all_pairs]


def read_input(filename: str) -> List[str]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    return content


def get_grid_size(points: List[List[Point]]) -> Tuple[int, int]:
    flattened = [p for point_pairs in points for p in point_pairs]
    max_y = max(flattened, key=lambda p: p.y).y
    max_x = max(flattened, key=lambda p: p.x).x
    return max_x + 1, max_y + 1


def get_lines(
    points: List[List[Point]],
) -> Tuple[List[List[Point]], List[List[Point]]]:
    """
    We sort the source and destination pairs. First by the x-coordinate, then
    by y. The function returns the point pairs into two different lists that
    represents the non_diagonal and diagonal lines.
    """
    non_diagonals = []
    diagonals = []
    for source, dest in points:
        point_pair = sorted([source, dest], key=lambda p1: (p1.x, p1.y))
        if source.x == dest.x or source.y == dest.y:
            non_diagonals.append(point_pair)
        else:
            diagonals.append(point_pair)

    return non_diagonals, diagonals


def mark_non_diagonal_line(
    grid: List[List[int]], source: Point, dest: Point
) -> List[List[int]]:
    """
    The 'smaller' point is source because we compare the x-coordinate before the y.
    If source.x == dest.x, we know that source.y < dest.y.
    """
    if source.x != dest.x:
        for j in range(source.x, dest.x + 1):
            grid[source.y][j] += 1
    else:
        for i in range(source.y, dest.y + 1):
            grid[i][source.x] += 1

    return grid


def mark_diagonal_line(
    grid: List[List[int]], source: Point, dest: Point
) -> List[List[int]]:
    """
    We know that the Point with a smaller x value is source.
    So we just need to check if source.y needs to be moved up or down.
    """
    curr_x = source.x
    if source.y < dest.y:
        for i in range(source.y, dest.y + 1):
            grid[i][curr_x] += 1
            curr_x += 1
    else:
        for i in range(source.y, dest.y - 1, -1):
            grid[i][curr_x] += 1
            curr_x += 1

    return grid


def count_overlapping_lines(grid: List[List[int]]) -> int:
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > 1:
                count += 1

    return count


def part_1(points: List[List[Point]]) -> int:
    max_x, max_y = get_grid_size(points)
    non_diagonals, _ = get_lines(points)
    grid = [[0 for _ in range(max_x)] for _ in range(max_y)]

    for source, dest in non_diagonals:
        grid = mark_non_diagonal_line(grid, source, dest)

    return count_overlapping_lines(grid)


def part_2(points: List[List[Point]]) -> int:
    max_x, max_y = get_grid_size(points)
    non_diagonals, diagonals = get_lines(points)
    grid = [[0 for _ in range(max_x)] for _ in range(max_y)]

    for source, dest in non_diagonals:
        grid = mark_non_diagonal_line(grid, source, dest)

    for source, dest in diagonals:
        grid = mark_diagonal_line(grid, source, dest)

    return count_overlapping_lines(grid)


if __name__ == "__main__":
    content = read_input("input.txt")
    points = get_list_of_points(content)
    print(part_1(points))
    print(part_2(points))
