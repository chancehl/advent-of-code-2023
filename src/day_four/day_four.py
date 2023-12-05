import os
from typing import List


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        nums = [line.strip() for line in f]

        return nums


def compute_score(nums: (List[int], List[int])) -> int:
    (owned, winning) = nums

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


def find_matches(nums: (List[int], List[int])) -> int:
    matches = 0

    for num in nums[0]:
        if num in nums[1]:
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
        score += compute_score(parse_numbers(line))

    return score


def part_two(input: List[str]) -> int:
    processed = []
    copies = []

    for index, line in enumerate(input):
        # find matches
        matches = find_matches(parse_numbers(line))

        # add copies to array
        for subindex in range(index + 1, index + 1 + matches):
            copies.append(subindex)

        # find and process existing copies
        matching_copies = list(filter(lambda c: c == index, copies))

        if len(matching_copies) > 0:
            for copy in matching_copies:
                for subindex in range(index + 1, index + 1 + matches):
                    copies.append(subindex)

                processed.append(copy)

        # mark as processed
        processed.append(index)

    return len(processed)


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
