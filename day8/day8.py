from collections import defaultdict
from typing import List, Pattern, Set, Dict
from pathlib import Path


def read_input(filename: str) -> List[str]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    content = [row.split("|") for row in content]
    content = [[inp.split(" ") for inp in row] for row in content if row]
    return content


def part_1(content: List[str]) -> int:
    """
    The easy digits: 1, 4, 7 and 8 each has a unique length.
    So we can simply find the easy digits by counting up each time
    a signal pattern with those lengths appears in the output.
    """
    unique_lens = set([2, 3, 4, 7])
    count = 0
    for _, output in content:
        for digit in output:
            if len(digit) in unique_lens:
                count += 1

    return count


def pattern_to_num_map(curr_inp: List[str]) -> Dict[str, str]:
    """
    From the problem description, we know that each number has a unique pattern
    associated with it. Specifically, each number is uniquely identified by
    a set of characters. I.e the order of the characters doesn't matter to
    identify the specific number.
    So first, we can find the "easy" numbers: 1, 4, 7 and 8 as the length of
    the pattern that represents these numbers are unique. Using the length of
    the "easy" numbers and the specific character -> int mapping that they
    each have, we can find all the other numbers by combining the mapping of
    the "easy" numbers in certain ways.
    Specifically, we can read from the problem description that one (of possibly
    many) mapping can look like:
    0 -> [0, 1, 2, 4, 5, 6]
    1 -> [2, 5] ***
    2 -> [0, 2, 3, 4, 6]
    3 -> [0, 2, 3, 5, 6]
    4 -> [1, 2, 3, 5] ***
    5 -> [0, 1, 3, 5, 6]
    6 -> [0, 1, 3, 4, 5, 6]
    7 -> [0, 2, 5] ***
    8 -> [0, 1, 2, 3, 4, 5, 6] ***
    9 -> [0, 1, 2, 3, 5, 6]
    where *** denotes that the pattern has a unique length.

    For instance, we know that the numbers: 0, 6 and 9 all are identified by
    a pattern with a length == 6.
    So to identify the pattern for number 9 if the current pattern represents 9
    and we perform:
    set.difference(nine_pattern, four) == [0, 6] which has a length of 2.
    Doing this operation on any other of the patterns with length 6, will
    result in a set with length 3.

    And we can continue performing the relevant set operations that uniquely
    identify each of the other numbers.

    When we store the pattern in the dictionary, we sort the string so that
    when the pattern is looked up, we can find the relevant key.
    Because "abc" != "bac". That means that the client code  must also sort the
    key before looking up the corresponding number.
    """
    pattern_to_num = defaultdict(int)
    one = seven = four = eight = set()
    for pattern in curr_inp:
        pattern = sorted(pattern)
        pattern = "".join(pattern)
        if len(pattern) == 2:
            one = set(pattern)
            pattern_to_num[pattern] = "1"
        elif len(pattern) == 3:
            seven = set(pattern)
            pattern_to_num[pattern] = "7"
        elif len(pattern) == 4:
            four = set(pattern)
            pattern_to_num[pattern] = "4"
        elif len(pattern) == 7:
            eight = set(pattern)
            pattern_to_num[pattern] = "8"

    for pattern in curr_inp:
        pattern = sorted(pattern)
        pattern = "".join(pattern)
        pattern_set = set(pattern)
        if len(pattern) == 6:
            curr_pattern = pattern_set - four
            if len(curr_pattern) == 2:
                pattern_to_num[pattern] = "9"

            elif len(pattern_set - seven) == 3:
                pattern_to_num[pattern] = "0"
            else:
                pattern_to_num[pattern] = "6"

        elif len(pattern) == 5:
            eight_minus_four = eight - four
            four_minus_one = four - one
            if len(pattern_set - eight_minus_four) == 2:
                pattern_to_num[pattern] = "2"
            elif (
                len(pattern_set - eight_minus_four) == 3
                and len(pattern_set - four_minus_one) == 3
            ):
                pattern_to_num[pattern] = "5"
            else:
                pattern_to_num[pattern] = "3"

    return pattern_to_num


def part_2(content: List[str]) -> int:
    total_sum = 0
    for input, output in content:
        curr_num = ""
        nums = pattern_to_num_map(input)

        for pattern in output:
            if pattern:
                inp = "".join(sorted(pattern))
                curr_num += nums[inp]

        total_sum += int(curr_num)

    return total_sum


if __name__ == "__main__":
    content = read_input("input.txt")
    print(f"part 1: {part_1(content)}")
    print(f"part 2: {part_2(content)}")
