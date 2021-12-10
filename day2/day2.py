from typing import List
from pathlib import Path


class Movement:
    def __init__(self, direction: str, dist: int):
        self.direction = direction
        self.dist = dist

    def __repr__(self) -> str:
        return f"{self.direction}: {self.dist}"


def read_input() -> List[Movement]:
    path_to_input = Path(__file__).parent / "input.txt"
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    content = [row.split(" ") for row in content]
    content = [Movement(row[0], int(row[1])) for row in content]
    return content


def part_1(content: List[Movement]) -> int:
    horizontal = 0
    vertical = 0
    for move in content:
        if move.direction == "down":
            vertical += move.dist
        elif move.direction == "up":
            vertical -= move.dist
        elif move.direction == "forward":
            horizontal += move.dist
        else:
            horizontal -= move.dist

    return vertical * horizontal


def part_2(content: List[Movement]) -> int:
    horizontal = 0
    vertical = 0
    aim = 0
    for move in content:
        if move.direction == "down":
            aim += move.dist
        elif move.direction == "up":
            aim -= move.dist
        elif move.direction == "forward":
            horizontal += move.dist
            vertical += move.dist * aim
        else:
            horizontal -= move.dist

    return vertical * horizontal


if __name__ == "__main__":
    content = read_input()
    print(f"part 1: {part_1(content)}")
    print(f"part 2: {part_2(content)}")
