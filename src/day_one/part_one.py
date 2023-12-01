import os
import re
from typing import List


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        nums = [line.strip() for line in f]

        return nums


def part_one(input: List[str]) -> int:
    sum = 0

    for line in input:
        num_str = re.sub("[a-zA-Z]", "", line)

        if len(num_str) == 1:
            sum += int(num_str + num_str)
        else:
            first = num_str[0]
            last = num_str[-1]

            sum += int(first + last)

    return sum


if __name__ == "__main__":
    score = part_one(read_input())

    print(score)
