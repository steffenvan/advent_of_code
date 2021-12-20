from typing import List, Tuple, Set
from pathlib import Path
from collections import namedtuple
from prettytable import PrettyTable

FoldOp = namedtuple("FoldOp", ["dim", "pos"])
Point = namedtuple("Point", ["x", "y"])


def read_input(filename: str) -> Tuple[List[Point], List[FoldOp]]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    content = [row.split(",") for row in content]
    points = [Point(int(row[0]), int(row[1])) for row in content if len(row) == 2]
    fold_ops = [
        row[0][11:] for row in content if "fold" in row[0]
    ]  # keep only x=**int** or y=**num**
    fold_ops = [row.split("=") for row in fold_ops]  # e.g ['x', '5'] or ['y', '8']
    fold_ops = [FoldOp(row[0], int(row[1])) for row in fold_ops]

    return points, fold_ops


def boundaries(points: List[Point]) -> Tuple[int, int]:
    max_x = max(point.x for point in points)
    max_y = max(point.y for point in points)
    return max_x, max_y


def fold_x(points: Set[Point], fold_op: FoldOp) -> Set[Point]:
    new_points = set()
    for p in points:
        if p.x > fold_op.pos:
            dist = (p.x - fold_op.pos) * 2
            new_x = p.x - dist
            new_points.add(Point(new_x, p.y))
        else:
            new_points.add(p)

    return new_points


def fold_y(points: Set[Point], fold_op: FoldOp) -> Set[Point]:
    new_points = set()
    for p in points:
        if p.y > fold_op.pos:
            dist = (p.y - fold_op.pos) * 2
            new_y = p.y - dist
            new_points.add(Point(p.x, new_y))
        else:
            new_points.add(p)

    return new_points


def fold(points: List[Point], fold_ops: List[FoldOp], part_1: bool) -> Set[Point]:
    updated_points = points
    for i, fold_op in enumerate(fold_ops):
        if part_1 and i > 0:
            break

        new_points = set()
        if fold_op.dim == "x":
            new_points = fold_x(updated_points, fold_op)
        else:
            new_points = fold_y(updated_points, fold_op)

        updated_points = new_points

    return updated_points


def part_1(points: List[Point], fold_ops: List[FoldOp]) -> int:
    """
    The 'difficult' part of this exercise is to perform the fold correctly. 
    For instance, if we are folding upwards we can find the mirrored coordinate 
    across the corresponding axis by performing the operation: 
    
    new_y = point.y - (point.y - fold.pos) * 2

    Example:
    Let fold_op = FoldOp(dim='y', pos=7) and p = Point(x=3, y=9). Then:
    new_y = 9 - (9 - 7) * 2 
          = 9 - 4 = 5 
    Thus the new point point becomes:
    new_p = Point(p.x, new_y)
    """

    new_points = fold(points, fold_ops, True)
    return len(new_points)


def part_2(points: List[Point], fold_ops: List[FoldOp]) -> int:
    """
    Same approach as part_1, we just have to keep using the updated points, 
    which leads to a smaller and smaller grid. 
    """
    points = fold(points, fold_ops, False)
    max_x, max_y = boundaries(points)
    max_x, max_y = max_x + 1, max_y + 1
    grid = [["" for _ in range(max_x)] for _ in range(max_y)]

    for p in points:
        grid[p.y][p.x] = "#"

    p = PrettyTable()
    for row in grid:
        p.add_row(row)

    print(p.get_string(header=False, border=False))


if __name__ == "__main__":
    points, fold_ops = read_input("input.txt")
    print(f"part 1: {part_1(points, fold_ops)}")
    print(f"part 2: {part_2(points, fold_ops)}")
