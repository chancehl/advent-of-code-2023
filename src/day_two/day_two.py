import os
import re
from typing import Dict, List

red_cubes = 12
green_cubes = 13
blue_cubes = 14


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        games = [re.sub("Game \\d+:", "", line).strip() for line in f]

        return games


def count_die(s: str) -> Dict[str, List[int]]:
    reds = []
    greens = []
    blues = []

    # 6 blue; 1 green, 4 blue, 2 red; 2 blue, 2 red -> ["6 blue", "1 green, 4 blue, 2 red", "2 blue, 2 red"]
    sets = s.split("; ")

    for index, set in enumerate(sets):
        # "2 blue, 2 red" -> ["2 blue", "2 red"]
        dice = set.split(", ")

        for die in dice:
            # "2 blue" -> ["2", "blue"]
            parts = die.split(" ")

            num = int(parts[0])
            color = parts[1]

            if color == "red":
                reds.append(num)
            elif color == "green":
                greens.append(num)
            elif color == "blue":
                blues.append(num)
            else:
                raise Exception(f"Invalid color: {color}")

    return {"red": reds, "green": greens, "blue": blues}


def is_game_possible(dict: Dict[str, List[int]]) -> bool:
    for key in dict.keys():
        if key == "red":
            for count in dict["red"]:
                if count > red_cubes:
                    return False
        elif key == "green":
            for count in dict["green"]:
                if count > green_cubes:
                    return False
        elif key == "blue":
            for count in dict["blue"]:
                if count > blue_cubes:
                    return False

    return True


def part_one(input: List[str]) -> int:
    score = 0

    for index, game in enumerate(input):
        dice_dict = count_die(game)

        if is_game_possible(dice_dict):
            # the games are not zero indexed. the first ID is 1, so offset index by 1.
            score += index + 1

    return score


def part_two(input: List[str]) -> int:
    score = 0

    for game in input:
        dice_dict = count_die(game)

        minimum_required_reds = max(dice_dict["red"])
        minimum_required_greens = max(dice_dict["green"])
        minimum_required_blues = max(dice_dict["blue"])

        power = minimum_required_reds * minimum_required_greens * minimum_required_blues

        score += power

    return score


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
