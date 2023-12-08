import os
from typing import List, Dict
from typing_extensions import Self


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        lines = [line.strip() for line in f]

        return lines


def parse_directions(input: List[str]) -> List[str]:
    return list(input[0])


def construct_graph(input: List[str]) -> Dict:
    graph = {}

    raw_nodes = input[2:]

    for node in raw_nodes:
        value = node[0:3]
        left = node[7:10]
        right = node[12:15]

        graph[value] = (left, right)

    return graph


def part_one(input: List[str]) -> int:
    directions = parse_directions(input)
    graph = construct_graph(input)

    steps = 0
    current = "AAA"

    while current != "ZZZ":
        for direction in directions:
            if direction == "L":
                current = graph[current][0]
            else:
                current = graph[current][1]

            steps += 1

    return steps


def part_two(input: List[str]) -> int:
    return -1


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
