from collections import defaultdict
from typing import List, Tuple, Union, Dict


class BingoBoard:
    """
    This class represents each individual bingo board. Internally, it has its
    own representation of the original, along with a dictionary that maps from
    a bingo number to the (i, j) coordinate it is on the board.
    We also store a boolean 2D-list to represents the positions that have been
    marked.
    """

    def __init__(self, board: List[List[int]]):
        self.board = board
        self.num_to_coordinate = self._make_num_to_coordinate_map(board)
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
        curr_col = [row[y] for row in self.boolean_board]
        return all(curr_row) or all(curr_col)

    def sum_of_unmarked(self) -> int:
        unmarked_sum = 0
        for i in range(len(self.boolean_board)):
            for j in range(len(self.boolean_board[0])):
                if not self.boolean_board[i][j]:
                    unmarked_sum += int(self.board[i][j])

        return unmarked_sum

    def _make_num_to_coordinate_map(
        self, board: List[List[int]]
    ) -> Dict[int, Tuple[int, int]]:
        num_to_c_map = defaultdict(tuple)
        for i in range(len(board)):
            for j in range(len(board[0])):
                num = board[i][j]
                num_to_c_map[num] = (i, j)

        return num_to_c_map
