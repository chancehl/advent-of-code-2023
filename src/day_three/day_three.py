import os
import re
from typing import List, NamedTuple


class NumberMatch(NamedTuple):
    start: int
    end: int
    num: int
    row: int


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        nums = [line.strip() for line in f]

        return nums


def find_nums(input: List[str]) -> List[NumberMatch]:
    nums = []

    for row, line in enumerate(input):
        for match in re.finditer(r"\d+", line):
            start = match.start()
            end = match.end()

            nums.append(
                NumberMatch(start=start, end=end, num=int(line[start:end]), row=row)
            )

    return nums


def convert_input_to_matrix(input: List[str]) -> List[List[str]]:
    matrix = []

    for line in input:
        matrix.append(list(line))

    return matrix


def is_adjacent_to_symbol(num_match: NumberMatch, matrix: List[List[str]]) -> bool:
    # look up
    if num_match.row > 0:
        for index in range(num_match.start, num_match.end):
            if is_value_symbol(num_match.row - 1, index, matrix):
                return True

    # look left
    if num_match.start > 0:
        if is_value_symbol(num_match.row, num_match.start - 1, matrix):
            return True

    # look right
    if num_match.end < len(matrix[0]):
        if is_value_symbol(num_match.row, num_match.end, matrix):
            return True

    # look down
    if num_match.row < len(matrix) - 1:
        for index in range(num_match.start, num_match.end):
            if is_value_symbol(num_match.row + 1, index, matrix):
                return True

    # look diagonally up & left
    if num_match.row > 0 and num_match.start > 0:
        if is_value_symbol(num_match.row - 1, num_match.start - 1, matrix):
            return True

    # look diagonally up & right
    if num_match.row > 0 and num_match.end < len(matrix[0]):
        if is_value_symbol(num_match.row - 1, num_match.end, matrix):
            return True

    # look diagonally down & left
    if num_match.row < len(matrix) - 1 and num_match.start > 0:
        if is_value_symbol(num_match.row + 1, num_match.start - 1, matrix):
            return True

    # look diagonally down & right
    if num_match.row < len(matrix) - 1 and num_match.end < len(matrix[0]):
        if is_value_symbol(num_match.row + 1, num_match.end, matrix):
            return True

    return False


def is_value_symbol(row: int, col: int, matrix: List[List[str]]) -> bool:
    if row < 0 or col > len(matrix):
        raise Exception("Index out of bounds")

    value = matrix[row][col]

    return True if re.match(r"(\d+|\.)", value) is None else False


def part_one(input: List[str]) -> int:
    sum = 0
    nums = find_nums(input)
    matrix = convert_input_to_matrix(input)

    for num_match in nums:
        if num_match.num == 31:
            print(num_match)

        if is_adjacent_to_symbol(num_match, matrix):
            sum += num_match.num

    return sum


if __name__ == "__main__":
    score_one = part_one(read_input())
    # score_two = part_two(read_input())

    print(score_one)
