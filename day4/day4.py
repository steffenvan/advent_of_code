from collections import defaultdict
from typing import List, Tuple, Union, Dict
from pathlib import Path

# represent each board with a hash map. num -> coordinates.
# assuming a number can only appear once in each board.


class BingoBoard:
    """
    This class represents each individual bingo board. Internally, it has its
    own representation of the original, along with a dictionary that maps from 
    a bingo number to the (i, j) coordinate it is on the board. 
    We also store a boolean 2D-list to represents the positions that have been
    marked. 
    """

    def __init__(self, board: List[List[str]]):
        self.board = board
        self.num_to_coordinate = self._num_to_coordinate(board)
        self.boolean_board = [
            [False for _ in range(len(board[0]))] for _ in range(len(board))
        ]

    def mark(self, num: int) -> Union[Tuple[int, int], None]:
        """
        Returns the coordinates of the number in the board if the number 
        is in this board. 
        """
        if num in self.num_to_coordinate:
            x, y = self.num_to_coordinate[num]
            self.boolean_board[x][y] = True
            return x, y

        return None

    def has_won(self, x: int, y: int) -> bool:
        curr_row = self.boolean_board[x]
        column = [row[y] for row in self.boolean_board]
        return all(curr_row) or all(column)

    def sum_of_unmarked(self) -> int:
        unmarked_sum = 0
        for i in range(len(self.boolean_board)):
            for j in range(len(self.boolean_board[0])):
                if not self.boolean_board[i][j]:
                    unmarked_sum += int(self.board[i][j])

        return unmarked_sum

    def _num_to_coordinate(self, board: List[List[str]]) -> Dict[int, Tuple[int, int]]:
        num_to_c_map = defaultdict(tuple)
        for i in range(len(board)):
            for j in range(len(board[0])):
                num = board[i][j]
                num_to_c_map[num] = (i, j)

        return num_to_c_map


def read_input(filename: str) -> List[str]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    bingo_nums = [x for x in content[0].split(",")]
    return bingo_nums, content[2:]


def parse_board(boards: List[str]) -> List[List[str]]:
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
            curr_board.append(row)
        else:
            if curr_board:
                all_boards.append(curr_board)
                curr_board = []
    all_boards.append(curr_board)  # add the last board

    return all_boards


def part_1(bingo_nums: List[int], bingo_boards: List[BingoBoard]) -> int:
    for num in bingo_nums:
        for board in bingo_boards:
            c = board.mark(num)
            if c and board.has_won(c[0], c[1]):
                return board.sum_of_unmarked() * int(num)

    return 0


def part_2(bingo_nums: List[int], bingo_boards: List[BingoBoard]) -> int:
    winners = set()
    for num in bingo_nums:
        for board in bingo_boards:
            c = board.mark(num)
            if c and board.has_won(c[0], c[1]):
                winners.add(board)
                # last winning board
                if len(winners) == len(bingo_boards):
                    return board.sum_of_unmarked() * int(num)
    return 0


if __name__ == "__main__":
    bingo_nums, boards = read_input("input.txt")
    all_boards = parse_board(boards)
    all_boards = [BingoBoard(board) for board in all_boards]

    print(f"part 1: {part_1(bingo_nums, all_boards)}")
    print(f"part 2: {part_2(bingo_nums, all_boards)}")
