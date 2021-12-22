from typing import List, Tuple, Dict
from pathlib import Path
from collections import Counter, defaultdict


def read_input(filename: str) -> Tuple[str, List[List[str]]]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readlines()

    content = [row.strip("\n") for row in content]
    polymer = content[0]

    rules = [row.split(" -> ") for row in content[2:]]
    rules = {row[0]: row[1] for row in rules}
    return polymer, rules


def get_char_counts(
    polymer: str, rules: Dict[str, str], num_iter: int
) -> Dict[str, int]:
    """Find the character counts for the final polymer. 

    Instead of building up the actual consecutive polymers, we can simply keep 
    track of the counts of the chars that make up the polymers. 
    
    To count the numbers of each character, we simply increment the count for
    each character in the key in the pair_count dictionary. Note that this will
    double count the elements *in the middle*. But not the start and end 
    characters. So to fix this, we will have to add one count for each of them. 
    Thanks to @DaniellVan for spotting this.     

    Example:
        If our template is "NNCB" and the rules state: 
        {
            "NN" -> "C"
                ...
        }
        we know that the first pair: "NN" should become: "NCN".
        Since "NN" appears once, we know that the new substrings will have counts:
        "NC" : 1
        "CN" : 1

    Args:
        polymer: the template polymer
        rules: the mappings from pairs to single chars
        num_iter: number of iterations we should build the polymer. 

    Returns:
        The counts for each character in the final polymer after 
        `num_iter` steps. 
    """
    pair_counts = defaultdict(int)
    char_counts = defaultdict(int)

    for pair in zip(polymer[:-1], polymer[1:]):
        pair_counts["".join(pair)] += 1

    for _ in range(num_iter):
        temp = defaultdict(int)
        for pair, count in pair_counts.items():
            middle = rules[pair]
            temp[pair[0] + middle] += count
            temp[middle + pair[1]] += count

        pair_counts = temp

    for pair, count in pair_counts.items():
        char_counts[pair[0]] += count
        char_counts[pair[1]] += count

    char_counts[polymer[0]] += 1
    char_counts[polymer[-1]] += 1

    return char_counts


def part_1(polymer: str, rules: List[List[str]]) -> int:
    char_counts = get_char_counts(polymer, rules, 10)
    return (max(char_counts.values()) - min(char_counts.values())) // 2


def part_2(polymer: str, rules: List[List[str]]) -> int:
    char_counts = get_char_counts(polymer, rules, 40)
    return (max(char_counts.values()) - min(char_counts.values())) // 2


if __name__ == "__main__":
    polymer, rules = read_input("input.txt")
    print(f"part 1: {part_1(polymer, rules)}")
    print(f"part 2: {part_2(polymer, rules)}")
