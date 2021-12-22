from typing import List
from pathlib import Path
from collections import defaultdict


class Fish:
    def __init__(self, timer: int, freeze: int = 0):
        self.timer = timer
        self.freeze_timer = freeze

    def decay(self):
        if self.timer >= 1:
            self.timer -= 1
            return self.timer == 0

    def is_alive(self) -> bool:
        return self.timer > 0

    def defrost(self):
        self.freeze_timer -= 1

    def is_frozen(self):
        return self.freeze_timer > 0

    def revive(self):
        self.timer = 6

    def __repr__(self):
        return f"({self.timer})"


def read_input(filename: str) -> List[str]:
    path_to_input = Path(__file__).parent / filename
    with open(path_to_input) as f:
        content = f.readline()

    content = content.split(",")
    content = [int(x) for x in content]
    return content


def part_1(content: List[int]) -> int:
    """
    The solution in part_2 is much faster, but keeping this for demonstration 
    purposes. 

    This method basically stores all the fish objects in a list, and keeps 
    adding the new fish to the list. It's very inefficient, and becomes 
    infeasible when we increase the number of iterations. 
    """
    all_fish = [Fish(x) for x in content]
    for _ in range(79):
        new_counter = 0
        for fish in all_fish:
            if fish.is_frozen():
                fish.defrost()
            else:
                if fish.is_alive():
                    just_died = fish.decay()
                    if just_died:
                        new_counter += 1
                else:
                    fish.revive()

        for _ in range(new_counter):
            all_fish.append(Fish(8, freeze=1))

    return len(all_fish)


def part_2(content: List[int]) -> int:
    """
    Instead of storing all of the actual fish and their timers, we can simply 
    use a dictionary to keep track of the *counts* of the different fish with a 
    specific timer, and change them all directly. 
    """
    counts = defaultdict(int)
    for timer in content:
        counts[timer] += 1

    for i in range(256):
        # store the intermediate updates so we don't modify the original
        # dictionary.
        temp = defaultdict(int)
        for timer, count in sorted(counts.items(), reverse=True):
            if timer >= 1:
                new_timer = timer - 1
                temp[new_timer] += count
                temp[timer] -= count
            else:
                temp[timer] -= count
                temp[6] += count
                temp[8] += count

        for timer, count in temp.items():
            counts[timer] += count

    return sum(counts.values())


if __name__ == "__main__":
    content = read_input("input.txt")
    print(f"part 1: {part_1(content)}")
    print(f"part 2: {part_2(content)}")

