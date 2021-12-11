from typing import List
from pathlib import Path
from collections import defaultdict


def read_input(input: str) -> List[str]:
    path_to_input = Path(__file__).parent / input
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    content = [list(x) for x in content]
    return content


# TODO: probably a very inefficient method to transpose a matrix. Fix later.
def transpose(matrix: List[List[int]]) -> List[List[int]]:
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = []

    for j in range(cols):
        curr_col = []
        for i in range(rows):
            curr_col.append(matrix[i][j])

        transposed.append(curr_col)

    return transposed


def count_ones(row: List[str]) -> int:
    count = 0
    for element in row:
        if element == "1":
            count += 1
    return count


def part_1(content: List[str]) -> int:
    """
    1. Tranpose the input. 
    2. Build up the binary gamma rate number by following the given rule.
    3. Find the epsilon rate by XOR'ing with only ones. 
    4. Multiply their decimal representation. 
    """
    content_T = transpose(content)
    cols = len(content_T[0])
    gamma_rate_bin = ""
    for row in content_T:
        num_ones = count_ones(row)
        if num_ones > cols - num_ones:  # if there is a majority of ones
            gamma_rate_bin += "1"
        else:
            gamma_rate_bin += "0"

    gamma_rate_dec = int(gamma_rate_bin, 2)
    ones = "1" * len(gamma_rate_bin)
    epsilon_rate_dec = int(gamma_rate_bin, 2) ^ int(ones, 2)

    return gamma_rate_dec * epsilon_rate_dec


def most_common_bit_incl(matrix: List[List[str]], pos: int) -> str:
    rows = len(matrix)
    num_ones = 0
    for i in range(rows):
        if matrix[i][pos] == "1":
            num_ones += 1

    return "1" if num_ones >= rows - num_ones else "0"


def get_nums_with_bit_in_pos(
    matrix: List[List[str]], pos: int, bit: str
) -> List[List[str]]:
    rows = len(matrix)
    correct_nums = []
    for i in range(rows):
        if matrix[i][pos] == bit:
            correct_nums.append(matrix[i])

    return correct_nums


def get_oxygen_rating(matrix: List[List[str]], pos: int) -> List[List[str]]:
    if len(matrix) == 1:
        return matrix

    mc_bit = most_common_bit_incl(matrix, pos)
    nums = get_nums_with_bit_in_pos(matrix, pos, mc_bit)
    return get_oxygen_rating(nums, pos + 1)


def get_c02_rating(matrix: List[List[str]], pos: int) -> List[List[str]]:
    """
    The least common bit is just the opposite of the most common bit. 
    """
    if len(matrix) == 1:
        return matrix

    mc_bit = most_common_bit_incl(matrix, pos)
    lc_bit = "0" if mc_bit == "1" else "1"
    nums = get_nums_with_bit_in_pos(matrix, pos, lc_bit)

    return get_c02_rating(nums, pos + 1)


def to_dec(bit: str) -> int:
    return int("".join(bit), 2)


def part_2(content: List[List[str]]) -> int:
    """
    Follow the rule of finding the most common/least common bit in each column.
    The least common is simply the opposite of the most common bit, so we can
    simply reuse the code there.  
    get_oxygen_rating() and get_c02_rating both returns a List[List[str]]. 
    Since we assume that all the binary numbers in the input is unique, we know
    that these functions return a List[List[str]] with one element in the end. 
    """

    oxygen_rating = get_oxygen_rating(content, 0)[0]
    c02_rating = get_c02_rating(content, 0)[0]

    return to_dec(oxygen_rating) * to_dec(c02_rating)


if __name__ == "__main__":
    content = read_input("input.txt")
    print(f"part 1: {part_1(content)}")
    print(f"part 2: {part_2(content)}")
