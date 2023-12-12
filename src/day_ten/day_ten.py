import os
from queue import Queue
from typing import List
from typing_extensions import Self


class PipeMazeNode:
    # honestly I hate having to track this across nodes but I'm too lazy to refactor this out
    _matrix: List[List[str]]
    position: (int, int)

    def __init__(self, matrix: List[List[str]], position: (int, int)) -> None:
        self._matrix = matrix
        self.position = position

    def __str__(self) -> str:
        return f"({self.position[0]}, {self.position[1]}) {self._matrix[self.position[0]][self.position[1]]}"

    def calculate_connections(self) -> ((int, int), (int, int)):
        (row, col) = self.position

        symbol = self._matrix[row][col]

        # N + S
        if symbol == "|":
            north_node = None
            south_node = None

            if row > 1:
                north_node = (row - 1, col)

            if row < len(self._matrix):
                south_node = (row + 1, col)

            return (north_node, south_node)
        # E + W
        elif symbol == "-":
            east_node = None
            west_node = None

            if col < len(self._matrix[0]):
                east_node = (row, col + 1)

            if col > 1:
                west_node = (row, col - 1)

            return (east_node, west_node)
        # N + E
        elif symbol == "L":
            north_node = None
            east_node = None

            if row > 1:
                north_node = (row - 1, col)

            if col < len(self._matrix[0]):
                east_node = (row, col + 1)

            return (north_node, east_node)
        # N + W
        elif symbol == "J":
            north_node = None
            west_node = None

            if row > 1:
                north_node = (row - 1, col)

            if col > 1:
                west_node = (row, col - 1)

            return (north_node, west_node)
        # S + W
        elif symbol == "7":
            south_node = None
            west_node = None

            if row < len(self._matrix):
                south_node = (row + 1, col)

            if col > 1:
                west_node = (row, col - 1)

            return (south_node, west_node)
        # S + E
        elif symbol == "F":
            south_node = None
            east_node = None

            if row < len(self._matrix):
                south_node = (row + 1, col)

            if col < len(self._matrix[0]):
                east_node = (row, col + 1)

            return (south_node, east_node)
        elif symbol == ".":
            return (None, None)
        elif symbol == "S":
            return (None, None)
        else:
            raise Exception(f"Invalid symbol: {symbol}")

    def compute_distance_from_root(self, visited: List[int] = []) -> int:
        symbol = self._matrix[self.position[0]][self.position[1]]

        print("Computing distance for", symbol)

        queue = Queue()

        # mark self as visited
        visited.append(self.position)

        # enqueue self
        queue.put(self.position)

        # loop
        while not queue.empty():
            # pop from queue
            current = queue.get()

            # calculate connections
            connections = PipeMazeNode(self._matrix, current).calculate_connections()

            # connection 0
            if connections[0] != None and connections[0] not in visited:
                queue.put(connections[0])

                visited.append(connections[0])

            # connection 1
            if connections[1] != None and connections[1] not in visited:
                queue.put(connections[1])

                visited.append(connections[1])

        return -1


class PipeMaze:
    nodes: List[PipeMazeNode]

    def __init__(self, nodes: List[PipeMazeNode]) -> None:
        self.nodes = nodes

    @staticmethod
    def from_matrix(matrix: List[List[str]]) -> Self:
        nodes = []

        for row in range(0, len(matrix)):
            for col in range(0, len(matrix[0])):
                nodes.append(PipeMazeNode(matrix, (row, col)))

        return PipeMaze(nodes=nodes)


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
        # print(node, node.compute_distance_from_root())
        max_distance = max(
            max_distance,
            node.compute_distance_from_root(visited=[]),
        )

    return max_distance


def part_two(input: List[str]) -> int:
    return -1


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
