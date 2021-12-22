from typing import List
from pathlib import Path


def read_input(filename: str) -> List[str]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readline()

    content = content.split(",")
    content = [int(num) for num in content]

    return content


def partial_sum(n: int) -> int:
    return (n * (n + 1)) // 2


def linear_search(content: List[int], is_part_1: bool) -> int:
    right = max(content)
    left = min(content)
    min_dist = right * right * len(content)

    for i in range(left, right + 1):
        curr_dist = 0
        for num in content:
            distance = abs(num - i) if is_part_1 else partial_sum(abs(num - i))
            curr_dist += distance

        min_dist = min(min_dist, curr_dist)

    return min_dist


def part_1(content: List[str]) -> int:
    return linear_search(content, True)


def part_2(content: List[str]) -> int:
    """
    Instead of using the distance, we just need to use the *partial sum* of the
    distance between position (a, b).
    """
    return linear_search(content, False)


if __name__ == "__main__":
    content = read_input("input.txt")
    print(f"part 1: {part_1(content)}")
    print(f"part 2: {part_2(content)}")
