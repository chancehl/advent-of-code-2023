import os
import sys
from typing import List, Dict, Tuple, Optional
from typing_extensions import Self
from numpy import Inf


class PipeMaze:
    graph: Dict
    matrix: List[List[str]]

    def __init__(self: Self, matrix: List[List[str]]) -> None:
        graph = {}

        self.matrix = matrix

        for row in range(0, len(matrix)):
            for col in range(0, len(matrix[0])):
                if matrix[row][col] != ".":
                    graph[(row, col)] = self.get_adjacent_nodes((row, col))

        self.graph = graph

    def get_adjacent_nodes(self: Self, position: (int, int)) -> (Tuple, Tuple):
        (row, col) = position

        symbol = self.matrix[row][col]

        nodes = []

        # N + S
        if symbol == "|":
            if row >= 1:
                nodes.append((row - 1, col))

            if row < len(self.matrix):
                nodes.append((row + 1, col))

            return nodes
        # E + W
        elif symbol == "-":
            if col < len(self.matrix[0]):
                nodes.append((row, col + 1))

            if col >= 1:
                nodes.append((row, col - 1))

            return nodes
        # N + E
        elif symbol == "L":
            if row >= 1:
                nodes.append((row - 1, col))

            if col < len(self.matrix[0]):
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
            if row < len(self.matrix):
                nodes.append((row + 1, col))

            if col >= 1:
                nodes.append((row, col - 1))

            return nodes
        # S + E
        elif symbol == "F":
            if row < len(self.matrix):
                nodes.append((row + 1, col))

            if col < len(self.matrix[0]):
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
            if self.matrix[key[0]][key[1]] == "S":
                return key

        return None

    def dijkstras(self: Self, start: (int, int)) -> Dict:
        # mark everything as unvisited
        unvisited_nodes = list(self.graph.keys())

        shortest_path = {}
        previous_nodes = {}

        max_value = Inf

        # set everything as "infinity" originally
        for node in unvisited_nodes:
            shortest_path[node] = max_value

        # starting node distance gets set to 0
        shortest_path[start] = 0

        while unvisited_nodes:
            current_min_node = None

            for node in unvisited_nodes:
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

            neighbors = self.get_adjacent_nodes(current_min_node)

            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + 1

                if (
                    neighbor in shortest_path
                    and tentative_value < shortest_path[neighbor]
                ):
                    shortest_path[neighbor] = tentative_value
                    previous_nodes[neighbor] = current_min_node

            unvisited_nodes.remove(current_min_node)

        return shortest_path

    def get_connecting_nodes(self: Self, node: (int, int)) -> Tuple:
        (row, col) = node

        symbol = self.matrix[row][col]

        # if it's the starting symbol, we're just going to look for any two connecting nodes
        if symbol == "S":
            nodes = []

            # up
            if row > 0 and self.matrix[row - 1][col] != ".":
                nodes.append((row - 1, col))

            # down
            if row < len(self.matrix) and self.matrix[row + 1][col] != ".":
                nodes.append((row + 1, col))

            # left
            if col > 0 and self.matrix[row][col - 1] != ".":
                nodes.append((row, col - 1))

            # right
            if col < len(self.matrix[0]) and self.matrix[row][col + 1] != ".":
                nodes.append((row, col + 1))

            return nodes
        else:
            connections = {
                "-": [(0, -1), (0, 1)],
                "|": [(-1, 0), (1, 0)],
                "L": [(-1, 0), (0, 1)],
                "J": [(-1, 0), (0, -1)],
                "7": [(1, 0), (0, -1)],
                "F": [(1, 0), (0, 1)],
                ".": [],
            }

            moves = connections[symbol]

            nodes = []

            for move in moves:
                nodes.append((row + move[0], col + move[1]))

            return nodes


def find_first_unvisited_connection(
    connections: List[Tuple], visited: List[Tuple]
) -> Tuple:
    for connection in connections:
        if connection not in visited:
            return connection

    return None


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        lines = [line.strip() for line in f]

        return lines


def part_one(input: List[str]) -> int:
    maze = PipeMaze([list(line) for line in input])

    start_node = maze.find_start_node()

    connecting_nodes = maze.get_connecting_nodes(start_node)

    left_node = connecting_nodes[0]
    right_node = connecting_nodes[1]

    left_visited = [start_node]
    right_visited = [start_node]

    distance = 1

    while left_node != right_node:
        left_visited.append(left_node)
        right_visited.append(right_node)

        left_connections = maze.get_connecting_nodes(left_node)
        right_connections = maze.get_connecting_nodes(right_node)

        next_left = find_first_unvisited_connection(left_connections, left_visited)
        next_right = find_first_unvisited_connection(right_connections, right_visited)

        left_node = next_left
        right_node = next_right

        distance += 1

    return distance


def part_two(input: List[str]) -> int:
    return -1


if __name__ == "__main__":
    # lol it's been about two days since adventofcode has fried my CPU
    sys.setrecursionlimit(50000)

    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
