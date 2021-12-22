from typing import List, Union, Tuple
from pathlib import Path
from bingo_board import BingoBoard


def read_input(filename: str) -> Tuple[List[int], List[str]]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    bingo_nums = [int(x) for x in content[0].split(",")]

    return bingo_nums, content[2:]


def parse_board(boards: List[str]) -> List[List[int]]:
    """
    Because of the way we parse the input, we know that each board is separated
    by an empty string. So when the curr row is empty, the next non-empty row
    will be a new board.
    """
    all_boards = []
    curr_board = []
    for curr_row in boards:
        if curr_row:
            row = curr_row.split(" ")
            row = list(filter(lambda x: len(x) > 0, row))
            row = [int(x) for x in row]
            curr_board.append(row)
        else:
            if curr_board:
                all_boards.append(curr_board)
                curr_board = []
    all_boards.append(curr_board)  # add the last board

    return all_boards


def part_1(bingo_nums: List[int], bingo_boards: List[BingoBoard]) -> Union[int, None]:
    for num in bingo_nums:
        for board in bingo_boards:
            coord = board.mark(num)
            if coord and board.has_won(coord[0], coord[1]):
                return board.sum_of_unmarked() * num

    return None


def part_2(bingo_nums: List[int], bingo_boards: List[BingoBoard]) -> Union[int, None]:
    """
    We find the last winner by adding all the winners to a set and check if
    the size of this set reaches the number of boards that are available.
    """
    winners = set()
    for num in bingo_nums:
        for board in bingo_boards:
            coord = board.mark(num)
            if coord and board.has_won(coord[0], coord[1]):
                winners.add(board)
                # last winning board
                if len(winners) == len(bingo_boards):
                    return board.sum_of_unmarked() * num

    return None


if __name__ == "__main__":
    bingo_nums, boards = read_input("input.txt")
    all_boards = parse_board(boards)
    all_boards = [BingoBoard(board) for board in all_boards]

    print(f"part 1: {part_1(bingo_nums, all_boards)}")
    print(f"part 2: {part_2(bingo_nums, all_boards)}")
