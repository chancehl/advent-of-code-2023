import os
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


def count_matches(nums: (List[int], List[int])) -> int:
    (owned, winning) = nums

    matches = 0

    for num in owned:
        if num in winning:
            matches += 1

    return matches


def parse_numbers(line: str) -> (List[int], List[int]):
    all_numbers = line.split(":")[1]  # always drop the 0th part ("Card N: ...")
    parts = all_numbers.split(" | ")

    owned_strs = list(filter(lambda s: len(s) > 0, parts[0].strip().split(" ")))
    owned = [int(num_str) for num_str in owned_strs]

    winning_strs = list(filter(lambda s: len(s) > 0, parts[1].strip().split(" ")))
    winning = [int(num_str) for num_str in winning_strs]

    return (owned, winning)


def part_one(input: List[str]) -> int:
    score = 0

    for line in input:
        (owned, winning) = parse_numbers(line)

        score += compute_score(owned, winning)

    return score


def part_two(input: List[str]) -> int:
    score = 0

    process_queue = []

    for index, line in enumerate(input):
        # append the current item to the queue
        process_queue.append(index)

        # parse the winning and owned numbers
        matches = count_matches(parse_numbers(line))

        print(matches)

    return score


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
