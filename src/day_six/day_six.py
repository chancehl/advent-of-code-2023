import os

from typing import List, Tuple


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        lines = [line.strip() for line in f]

        return lines


def parse_race_records(input: List[str]) -> List[Tuple]:
    raw_times = input[0]
    raw_distances = input[1]

    time_values = raw_times.split("Time:")[1]
    distance_values = raw_distances.split("Distance:")[1]

    times = [
        int(value) for value in filter(lambda s: len(s) > 0, time_values.split(" "))
    ]

    distances = [
        int(value) for value in filter(lambda s: len(s) > 0, distance_values.split(" "))
    ]

    return zip(times, distances)


def parse_race_record(input: List[str]) -> (int, int):
    raw_times = input[0]
    raw_distances = input[1]

    time_value = raw_times.split("Time:")[1]
    distance_value = raw_distances.split("Distance:")[1]

    time = int(time_value.strip().replace(" ", ""))
    distance = int(distance_value.strip().replace(" ", ""))

    return (time, distance)


def compute_ways_to_beat_record(race: (int, int)) -> int:
    (total_time, max_distance) = race

    ways = 0

    for hold_time in range(1, total_time):
        travel_time = total_time - hold_time
        total_distance = travel_time * hold_time

        if total_distance > max_distance:
            ways += 1

    return ways


def part_one(input: List[str]) -> int:
    races = parse_race_records(input)

    ways = 1

    for race in races:
        ways *= compute_ways_to_beat_record(race)

    return ways


def part_two(input: List[str]) -> int:
    race = parse_race_record(input)

    ways = compute_ways_to_beat_record(race)

    return ways


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
