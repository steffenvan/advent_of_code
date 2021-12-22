from typing import List


class Point:
    def __init__(self, pair: List[str]):
        self.x = int(pair[0])
        self.y = int(pair[1])

    def __repr__(self):
        return f"({self.x}, {self.y})"
