from pathlib import Path
from functools import reduce
from typing import List, Callable, Union, Tuple

from ast import Literal, Operator, ast_node


def read_input(filename: str) -> str:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readline()

    return content


def hex_to_bin(hex: str) -> str:
    return "".join(bin(int(c, 16))[2:].zfill(4) for c in hex if c != "\n")


def get_length_type_value(body: str, length_type_id: str) -> str:
    if length_type_id == "1":
        return body[:11]
    else:
        return body[:15]


def get_literal_body(bin_str: str, acc: str) -> str:
    """
    We use this to find scope of the literal packet. 
    """
    if bin_str[0] == "0":
        return acc + bin_str[:5]

    return get_literal_body(bin_str[5:], acc + bin_str[:5])


def is_literal(type_id: str) -> bool:
    return int(type_id, 2) == 4


def get_version_sum(bin_str: str, acc: int) -> str:
    if len(bin_str) < 16:
        return acc

    version = int(bin_str[:3], 2)
    type_id = bin_str[3:6]
    body = bin_str[6:] if is_literal(type_id) else bin_str[7:]
    curr_packet_str = bin_str[:6] if is_literal(type_id) else bin_str[:7]

    if is_literal(type_id):
        curr_packet_str += get_literal_body(body, "")
        next_packet = len(curr_packet_str)
        return get_version_sum(bin_str[next_packet:], acc + version)

    length_type_id = bin_str[6]
    curr_packet_str += get_length_type_value(body, length_type_id)

    return get_version_sum(bin_str[len(curr_packet_str) :], acc + version)


def get_operation(type_id: str) -> Callable[[int, int], Union[int, None]]:
    if type_id == "000":
        return lambda x, y: x + y
    elif type_id == "001":
        return lambda x, y: x * y
    elif type_id == "010":
        return lambda x, y: min(x, y)
    elif type_id == "011":
        return lambda x, y: max(x, y)
    elif type_id == "101":
        return lambda x, y: 1 if x > y else 0
    elif type_id == "110":
        return lambda x, y: 1 if x < y else 0
    elif type_id == "111":
        return lambda x, y: 1 if x == y else 0
    return None


def get_remaining_packets(packet: str) -> str:
    length_type_id = packet[6]
    body = packet[7:]
    curr_packet_str = packet[:7]
    curr_packet_str += get_length_type_value(body, length_type_id)
    return packet[len(curr_packet_str) :]


def get_children_and_remaining_packets(
    packet: str, length_type_id: str, remaining_packets: str
) -> List[ast_node]:
    """
    Only called by operator packets. Returns all the children of the operator
    node and the remaining nodes (if there are any). 
    """
    children = []
    if length_type_id == "1":
        length = int(packet[7 : 7 + 11], 2)
        for i in range(length):
            child, remaining_packets = parse(remaining_packets)
            children.append(child)
    else:
        length = int(packet[7 : 7 + 15], 2)
        body = remaining_packets[:length]
        while body:
            child, body = parse(body)
            children.append(child)

        remaining_packets = remaining_packets[length:]

    return children, remaining_packets


def parse(packet: str) -> Tuple[ast_node, str]:
    """
    This functions parses the whole binary string input into an AST. 

    Args:
        packet: the binary string that represents the packet. 

    Returns:
        curr_packet: the ast node that can be either a literal or an operator. 
        remaining_packets: the remaining packet str yet to be parsed.  
    """
    type_id = packet[3:6]
    if is_literal(type_id):
        curr_packet = packet[:6] + get_literal_body(packet[6:], "")
        remaining_packets = packet[len(curr_packet) :]
        return Literal(curr_packet), remaining_packets

    remaining_packets = get_remaining_packets(packet)
    length_type_id = packet[6]
    children, remaining_packets = get_children_and_remaining_packets(
        packet, length_type_id, remaining_packets
    )
    curr_packet = Operator(get_operation(type_id), children)

    return curr_packet, remaining_packets


def evaluate_ast(node: ast_node) -> int:
    if isinstance(node, Literal):
        return node.to_digit()

    return reduce(node.op, [evaluate_ast(child) for child in node.children])


def evaluate(packet: str) -> int:
    root, _ = parse(packet)
    return evaluate_ast(root)


def part_1(input: str) -> int:
    as_bin = hex_to_bin(input)
    return get_version_sum(as_bin, 0)


def part_2(hex_input: str) -> int:
    as_bin = hex_to_bin(hex_input)
    return evaluate(as_bin)


if __name__ == "__main__":
    content = read_input("input.txt")
    print(f"part 1: {part_1(content)}")
    print(f"part 2: {part_2(content)}")
