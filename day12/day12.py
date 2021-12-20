from collections import defaultdict
from os import urandom
from typing import List, Dict, Set
from pathlib import Path


def read_input(filename: str) -> List[str]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    content = [row.split("-") for row in content]
    return content


def build_graph(content: List[str]) -> Dict[str, List[str]]:
    graph = defaultdict(list)
    for parent, child in content:
        if parent != "end" or child != "start":
            graph[parent].append(child)
        if parent != "start" and child != "end":
            graph[child].append(parent)

    return graph


def dfs_part1(graph: Dict[str, List[str]], visited: Set[str], curr: str) -> int:
    if curr == "end":
        return 1

    if curr in visited:
        return 0

    if curr.islower():
        visited.add(curr)

    total_paths = 0
    for neighbour in graph[curr]:
        total_paths += dfs_part1(graph, visited, neighbour)

    if curr.islower():
        visited.remove(curr)

    return total_paths


def dfs_part2(graph: Dict[str, List[str]], visited: Dict[str, int], curr: str) -> int:

    # If we are currently visiting a small cave and have already visited a
    # small cave once. Or if we visit the same cave for the third time.
    if visited[curr] == 1 and 2 in visited.values() or visited[curr] == 2:
        return 0

    if curr == "end":
        return 1

    if curr.islower():
        visited[curr] += 1

    total_paths = 0
    for neighbour in graph[curr]:
        if neighbour != "start":
            total_paths += dfs_part2(graph, visited, neighbour)

    if visited[curr] > 0:
        visited[curr] -= 1

    return total_paths


def part_1(content: List[str]) -> int:
    """
    We use a standard recursive DFS to count the number of paths from 'start' 
    to 'end'. Use a hashset to keep track of the visited small caves. 
    """
    visited = set()
    graph = build_graph(content)
    return dfs_part1(graph, visited, "start")


def part_2(content: List[str]) -> int:
    """
    Almost similar to part_1, but use a hashmap to keep track of the currently
    visited small caves. If a small cave is being visited more than 2 times or
    we are visiting a small cave for the second time and another small cave has
    already been visited twice, we return 0 from that path. 
    """
    visited = defaultdict(int)
    graph = build_graph(content)
    return dfs_part2(graph, visited, "start")


if __name__ == "__main__":
    content = read_input("input.txt")
    print(f"part 1: {part_1(content)}")
    print(f"part 2: {part_2(content)}")
