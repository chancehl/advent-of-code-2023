import os
import re
from typing import List


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        nums = [line.strip() for line in f]

        return nums


def compute_score(owned: List[int], winning: List[int]) -> int:
    matches = []

    starting_score = 1
    total_score = 0

    for num in owned:
        if num in winning:
            matches.append(num)

    for num in range(0, len(matches)):
        total_score = starting_score
        starting_score = starting_score * 2

    return total_score


def parse_numbers(line: str) -> (List[int], List[int]):
    all_numbers = line.split(":")[1]  # always drop the 0th part ("Card N: ...")
    parts = all_numbers.split(" | ")

    owned_number_strs = list(filter(lambda s: len(s) > 0, parts[0].strip().split(" ")))
    owned_numbers = [int(num_str) for num_str in owned_number_strs]

    winning_number_strs = list(
        filter(lambda s: len(s) > 0, parts[1].strip().split(" "))
    )
    winning_numbers = [int(num_str) for num_str in winning_number_strs]

    return (owned_numbers, winning_numbers)


def part_one(input: List[str]) -> int:
    sum = 0

    for line in input:
        (owned_numbers, winning_numbers) = parse_numbers(line)

        sum += compute_score(owned_numbers, winning_numbers)

    return sum


if __name__ == "__main__":
    score_one = part_one(read_input())
    # score_two = part_two(read(input()))

    print(score_one)
