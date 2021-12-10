from typing import List
from pathlib import Path


def read_input() -> List[int]:
    path_to_input = Path(__file__).parent / "input.txt"
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    content = [int(row) for row in content]
    return content


def part_1(content: List[str]) -> int:
    incr = 0
    for i in range(1, len(content)):
        if content[i] > content[i - 1]:
            incr += 1
    return incr


def part_2(content: List[str]) -> int:
    sums = []
    for i in range(len(content) - 2):
        curr_sum = content[i] + content[i + 1] + content[i + 2]
        sums.append(curr_sum)

    return part_1(sums)


if __name__ == "__main__":
    content = read_input()
    print(f"part 1: {part_1(content)}")
    print(f"part 2: {part_2(content)}")
