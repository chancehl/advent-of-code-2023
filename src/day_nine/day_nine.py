import os
from typing import List


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        lines = [line.strip() for line in f]

        return lines


def computed_diffed_subsequence(nums: List[int]) -> List[int]:
    diffs = []

    for i in range(0, len(nums) - 1):
        diffs.append(nums[i + 1] - nums[i])

    return diffs


def compute_extrapolated_sequence(
    all_nums: List[List[int]], backwards: bool = False
) -> List[int]:
    if len(all_nums) < 2:
        raise Exception("Invalid number of sequences (min=2)")

    index = 0

    all_nums.reverse()

    while index < len(all_nums) - 1:
        a = all_nums[index]
        b = all_nums[index + 1]

        if backwards:
            b.insert(0, b[0] - a[0])
        else:
            b.append(a[-1] + b[-1])

        index += 1

    return [sequence[-1 if not backwards else 0] for sequence in all_nums]


def is_all_zeroes(nums: List[int]) -> bool:
    return all([num == 0 for num in nums])


def part_one(input: List[str]) -> int:
    score = 0

    for line in input:
        # convert to nums
        nums = [int(num) for num in line.split(" ")]

        # capture all subsequences
        subsequences = [nums]

        # compute this specific subsequence
        subsequence = computed_diffed_subsequence(nums)

        # repeat
        while not is_all_zeroes(subsequence):
            subsequences.append(subsequence)
            subsequence = computed_diffed_subsequence(subsequence)
        else:
            subsequences.append(subsequence)

        # extrapolate
        extrapolated_values = compute_extrapolated_sequence(subsequences)

        # sum
        score += extrapolated_values[-1]

    return score


def part_two(input: List[str]) -> int:
    score = 0

    for line in input:
        # convert to nums
        nums = [int(num) for num in line.split(" ")]

        # capture all subsequences
        subsequences = [nums]

        # compute this specific subsequence
        subsequence = computed_diffed_subsequence(nums)

        # repeat
        while not is_all_zeroes(subsequence):
            subsequences.append(subsequence)
            subsequence = computed_diffed_subsequence(subsequence)
        else:
            subsequences.append(subsequence)

        # extrapolate
        extrapolated_values = compute_extrapolated_sequence(
            subsequences, backwards=True
        )

        # sum
        score += extrapolated_values[-1]

    return score


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
