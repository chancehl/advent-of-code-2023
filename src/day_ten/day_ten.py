import os
import sys
from typing import List, Dict, Tuple, Optional
from typing_extensions import Self


class PipeMaze:
    graph: Dict
    _matrix: List[List[str]]

    def __init__(self: Self, matrix: List[List[str]]) -> None:
        graph = {}

        for row in range(0, len(matrix)):
            for col in range(0, len(matrix[0])):
                graph[(row, col)] = PipeMaze.get_adjacent_nodes(matrix, (row, col))

        self.graph = graph
        self._matrix = matrix

    @staticmethod
    def get_adjacent_nodes(
        matrix: List[List[str]], position: (int, int)
    ) -> (Tuple, Tuple):
        (row, col) = position

        symbol = matrix[row][col]

        nodes = []

        # N + S
        if symbol == "|":
            if row >= 1:
                nodes.append((row - 1, col))

            if row < len(matrix):
                nodes.append((row + 1, col))

            return nodes
        # E + W
        elif symbol == "-":
            if col < len(matrix[0]):
                nodes.append((row, col + 1))

            if col >= 1:
                nodes.append((row, col - 1))

            return nodes
        # N + E
        elif symbol == "L":
            if row >= 1:
                nodes.append((row - 1, col))

            if col < len(matrix[0]):
                nodes.append((row, col + 1))

            return nodes
        # N + W
        elif symbol == "J":
            if row >= 1:
                nodes.append((row - 1, col))

            if col >= 1:
                nodes.append((row, col - 1))

            return nodes
        # S + W
        elif symbol == "7":
            if row < len(matrix):
                nodes.append((row + 1, col))

            if col >= 1:
                nodes.append((row, col - 1))

            return nodes
        # S + E
        elif symbol == "F":
            if row < len(matrix):
                nodes.append((row + 1, col))

            if col < len(matrix[0]):
                nodes.append((row, col + 1))

            return nodes
        elif symbol == ".":
            return []
        elif symbol == "S":
            return []
        else:
            raise Exception(f"Invalid symbol: {symbol}")

    def find_start_node(self: Self) -> Optional[Tuple]:
        for key in self.graph.keys():
            if self._matrix[key[0]][key[1]] == "S":
                return key

        return None

    def find_shortest_path(
        self: Self, start: (int, int), end: (int, int), path: List[Tuple] = []
    ) -> List[Tuple]:
        path = path + [start]

        if start == end:
            return path

        if start not in self.graph:
            return None

        shortest = None

        for node in self.graph[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)

                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath

        return shortest


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        lines = [line.strip() for line in f]

        return lines


def part_one(input: List[str]) -> int:
    max_distance = -1

    maze = PipeMaze([list(line) for line in input])

    start = maze.find_start_node()

    for node in maze.graph:
        path = maze.find_shortest_path(start=node, end=start, path=[])

        if path != None:
            max_distance = max(max_distance, len(path) - 1)

    return max_distance


def part_two(input: List[str]) -> int:
    return -1


if __name__ == "__main__":
    # lol it's been about two days since adventofcode has fried my CPU
    sys.setrecursionlimit(50000)

    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
