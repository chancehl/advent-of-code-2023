import os
import re
from typing import List

numbers = {
    # overlaps
    "oneight": "18",
    "twone": "21",
    "threeight": "38",
    "fiveight": "58",
    "sevenine": "79",
    "eightwo": "82",
    "eighthree": "83",
    "nineight": "98",
    # digits
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def replace_numbers(s: str) -> str:
    for key in numbers.keys():
        if key in s:
            s = s.replace(key, numbers.get(key))

    return s


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        nums = [line.strip() for line in f]

        return nums


def part_two(input: List[str]) -> int:
    sum = 0

    for num_str in input:
        num = re.sub("[a-zA-Z]", "", replace_numbers(num_str))

        if len(num) == 1:
            sum += int(num + num)
        else:
            first = num[0]
            last = num[-1]

            sum += int(first + last)

    return sum


if __name__ == "__main__":
    score = part_two(read_input())

    print(score)
