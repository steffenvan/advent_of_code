from typing import List
from pathlib import Path


def read_input(filename: str) -> List[str]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    return content


def part_1(content: List[str]) -> int:
    """
    1. use a stack to add all the opening parenthesis we encounter
    2. if the curr charater is not a parenthesis, we know that it should match
    the most recent opening parenthesis, i.e the one on top of the stack. If it
    doesn't match, we can count the points that is specified in the problem
    statement.
    """
    total_point = 0
    for parenthesis in content:
        stack = []
        for c in parenthesis:
            if c == "(" or c == "[" or c == "{" or c == "<":
                stack.append(c)
            else:
                curr = stack.pop()

                if c == ")" and curr != "(":
                    total_point += 3
                    break
                elif c == "]" and curr != "[":
                    total_point += 57
                    break
                elif c == "}" and curr != "{":
                    total_point += 1197
                    break
                elif c == ">" and curr != "<":
                    total_point += 25137
                    break

    return total_point


def part_2(content: List[str]) -> int:
    """
    Following the rules we only consider the lines that have incomplete
    paranthesis and discard the invalid ones.
    """

    all_scores = []
    for input in content:
        stack = []
        curr_score = 0
        for c in input:
            if c == "(" or c == "[" or c == "{" or c == "<":
                stack.append(c)
            else:
                curr = stack[-1]
                if c == ")" and curr == "(":
                    stack.pop()
                elif c == "]" and curr == "[":
                    stack.pop()
                elif c == "}" and curr == "{":
                    stack.pop()
                elif c == ">" and curr == "<":
                    stack.pop()
                else:  # discard the lines with invalid parenthesis
                    stack = []
                    break

        while stack:
            curr_score *= 5
            curr = stack.pop()
            if curr == "(":
                curr_score += 1
            elif curr == "[":
                curr_score += 2
            elif curr == "{":
                curr_score += 3
            else:
                curr_score += 4

        if curr_score:
            all_scores.append(curr_score)

    mid = len(all_scores) // 2
    all_scores = sorted(all_scores)

    return all_scores[mid]


if __name__ == "__main__":
    content = read_input("input.txt")
    print(f"part 1: {part_1(content)}")
    print(f"part 2: {part_2(content)}")
