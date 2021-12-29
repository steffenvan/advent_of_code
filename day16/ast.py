from collections import namedtuple
from typing import Union


class Literal:
    def __init__(self, packet):
        self.header = packet[:6]
        self.body = packet[6:]

    def to_digit(self):
        value = get_value(self.body, "")
        return int(value, 2)

    def get_body_value(self, body, acc):
        """
        This function returns the binary value of the literal. 
        """


def get_value(body: str, acc: str) -> str:
    if body[0] == "0":
        return acc + body[1:5]

    return get_value(body[5:], acc + body[1:5])


Operator = namedtuple("Operator", ["op", "children"])
ast_node = Union[Operator, Literal]
