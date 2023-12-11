import os
from typing import List, Optional
from typing_extensions import Self


class PipeMazeNode:
    symbol: str
    position: (int, int)
    connections: (Self, Self)

    def __init__(
        self, symbol: str, position: (int, int), connections: (Self, Self)
    ) -> None:
        self.symbol = symbol
        self.position = position
        self.connections = connections

    def compute_distance_from_root() -> int:
        return -1


class PipeMaze:
    start: PipeMazeNode
    nodes: List[PipeMazeNode]

    def __init__(self, start: PipeMazeNode, nodes: List[PipeMazeNode]) -> None:
        self.start = start
        self.nodes = nodes

    @staticmethod
    def from_matrix(matrix: List[List[str]]) -> Self:
        start = None
        nodes = []

        for row in range(0, len(matrix)):
            for col in range(0, len(matrix[0])):
                connections = PipeMaze.calculate_connections((row, col))

                node = PipeMazeNode(
                    symbol=matrix[row][col],
                    position=(row, col),
                    connections=connections,
                )

                nodes.append(node)

                if node.symbol == "S":
                    start = node

                print(node)

        return PipeMaze(start=start, nodes=nodes)

    @staticmethod
    def calculate_connections(
        matrix: List[List[str]], position: (int, int)
    ) -> ((int, int), (int, int)):
        (row, col) = position

        symbol = matrix[row][col]

        # N + S
        if symbol == "|":
            north_node = None
            south_node = None

            if row > 1:
                north_node = (row - 1, col)

            if row < len(matrix):
                south_node = (row + 1, col)

            return (north_node, south_node)
        # E + W
        elif symbol == "-":
            east_node = None
            west_node = None

            if col < len(matrix[0]):
                east_node = (row, col + 1)

            return (east_node, west_node)
        # N + E
        elif symbol == "L":
            north_node = None
            east_node = None

            return (north_node, east_node)
        # N + W
        elif symbol == "J":
            north_node = None
            west_node = None

            return (north_node, west_node)
        # S + W
        elif symbol == "7":
            south_node = None
            west_node = None

            return (south_node, west_node)
        # S + E
        elif symbol == "F":
            south_node = None
            east_node = None

            return (south_node, east_node)
        elif symbol == ".":
            return (None, None)
        elif symbol == "S":
            return (None, None)
        else:
            raise Exception(f"Invalid symbol: {symbol}")


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input-b.txt")

    with open(file_loc) as f:
        lines = [line.strip() for line in f]

        return lines


def part_one(input: List[str]) -> int:
    raw_nodes = [list(line) for line in input]

    max_distance = -1

    maze = PipeMaze.from_matrix(raw_nodes)

    for node in maze.nodes:
        max_distance = max(max_distance, node.compute_distance_from_root())

    return max_distance


def part_two(input: List[str]) -> int:
    return -1


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
