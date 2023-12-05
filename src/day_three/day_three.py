import os
import re
from typing import List, NamedTuple
from enum import Enum


class NumberMatch(NamedTuple):
    start: int
    end: int
    num: int
    row: int


class AsteriskMatch(NamedTuple):
    start: int
    end: int
    row: int


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        lines = [line.strip() for line in f]

        return lines


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


def find_asterisks(input: List[str]) -> List[AsteriskMatch]:
    asterisks = []

    for row, line in enumerate(input):
        for match in re.finditer(r"\*", line):
            start = match.start()
            end = match.end()

            asterisks.append(AsteriskMatch(start=start, end=end, row=row))

    return asterisks


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


def is_value_number(row: int, col: int, matrix: List[List[str]]) -> bool:
    if row < 0 or col > len(matrix):
        raise Exception("Index out of bounds")

    value = matrix[row][col]

    return True if re.match(r"\d", value) is not None else False


def is_adjacent_to_two_nums(
    asterisk_match: AsteriskMatch, matrix: List[List[str]]
) -> bool:
    adjacent_nums = get_adjacent_nums(asterisk_match, matrix)

    return adjacent_nums is not None and len(adjacent_nums) == 2


def crawl_for_num(origin: (int, int), matrix: List[List[str]]) -> int:
    (row, col) = origin

    # grab contact point
    num_str = matrix[row][col]

    if not is_value_number(row, col, matrix):
        return None

    # crawl left
    if col > 0:
        col_index = col - 1

        while col_index > 0 and is_value_number(row, col_index, matrix):
            num_str = f"{matrix[row][col_index]}{num_str}"
            col_index -= 1

    # crawl right
    if col < len(matrix[0]):
        col_index = col + 1

        while col_index < len(matrix[0]) and is_value_number(row, col_index, matrix):
            num_str = f"{num_str}{matrix[row][col_index]}"
            col_index += 1

    return int(num_str)


def get_adjacent_num(
    asterisk_match: AsteriskMatch, direction: Direction, matrix: List[List[str]]
) -> int | None:
    if direction == Direction.UP:
        num = crawl_for_num((asterisk_match.row - 1, asterisk_match.start), matrix)

        return num
    if direction == Direction.DOWN:
        num = crawl_for_num((asterisk_match.row + 1, asterisk_match.start), matrix)

        return num
    if direction == Direction.LEFT:
        num = crawl_for_num((asterisk_match.row, asterisk_match.start - 1), matrix)

        return num
    if direction == Direction.RIGHT:
        num = crawl_for_num((asterisk_match.row, asterisk_match.end), matrix)

        return num
    if direction == Direction.UP_LEFT:
        num = crawl_for_num((asterisk_match.row - 1, asterisk_match.start - 1), matrix)

        return num
    if direction == Direction.UP_RIGHT:
        num = crawl_for_num((asterisk_match.row - 1, asterisk_match.end), matrix)

        return num
    if direction == Direction.DOWN_LEFT:
        num = crawl_for_num((asterisk_match.row + 1, asterisk_match.start - 1), matrix)

        return num
    if direction == Direction.DOWN_RIGHT:
        num = crawl_for_num((asterisk_match.row + 1, asterisk_match.end), matrix)

        return num

    return None


def get_adjacent_nums(
    asterisk_match: AsteriskMatch, matrix: List[List[str]]
) -> (int, int):
    up = get_adjacent_num(asterisk_match, Direction.UP, matrix)
    down = get_adjacent_num(asterisk_match, Direction.DOWN, matrix)
    left = get_adjacent_num(asterisk_match, Direction.LEFT, matrix)
    right = get_adjacent_num(asterisk_match, Direction.RIGHT, matrix)
    up_left = get_adjacent_num(asterisk_match, Direction.UP_LEFT, matrix)
    up_right = get_adjacent_num(asterisk_match, Direction.UP_RIGHT, matrix)
    down_left = get_adjacent_num(asterisk_match, Direction.DOWN_LEFT, matrix)
    down_right = get_adjacent_num(asterisk_match, Direction.DOWN_RIGHT, matrix)

    adjacent_nums = list(
        set(
            filter(
                lambda num: num is not None,
                [up, down, left, right, up_left, up_right, down_left, down_right],
            )
        )
    )

    if len(adjacent_nums) != 2:
        return None

    return (adjacent_nums[0], adjacent_nums[1])


def part_one(input: List[str]) -> int:
    score = 0
    nums = find_nums(input)
    matrix = convert_input_to_matrix(input)

    for num_match in nums:
        if is_adjacent_to_symbol(num_match, matrix):
            score += num_match.num

    return score


def part_two(input: List[str]) -> int:
    score = 0
    asterisks = find_asterisks(input)
    matrix = convert_input_to_matrix(input)

    for asterisk_match in asterisks:
        if is_adjacent_to_two_nums(asterisk_match, matrix):
            (a, b) = get_adjacent_nums(asterisk_match, matrix)

            score += a * b

    return score


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one)
