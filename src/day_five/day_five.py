import os
from typing import List, TypedDict


class FarmerMap(TypedDict):
    desintation_range_start: int
    source_range_start: int
    range_length: int


class Almanac(TypedDict):
    seed_to_soil: List[FarmerMap]
    soil_to_fertilizer: List[FarmerMap]
    fertilizer_to_water: List[FarmerMap]
    water_to_light: List[FarmerMap]
    light_to_temperature: List[FarmerMap]
    temperature_to_humidity: List[FarmerMap]
    humidity_to_location: List[FarmerMap]


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input.txt")

    with open(file_loc) as f:
        lines = [line.strip() for line in f]

        return lines


def create_maps_from_slice(slice: List[str]) -> List[FarmerMap]:
    maps = []

    for line in slice:
        parts = line.split(" ")

        maps.append(
            FarmerMap(
                desintation_range_start=int(parts[0]),
                source_range_start=int(parts[1]),
                range_length=int(parts[2]),
            )
        )

    return maps


def parse_almanac(input: List[str]) -> Almanac:
    almanac = Almanac()

    # seed to soil
    almanac["seed_to_soil"] = create_maps_from_slice(input[3:19])

    # soil to fertilizer
    almanac["soil_to_fertilizer"] = create_maps_from_slice(input[21:39])

    # fertilizer to water
    almanac["fertilizer_to_water"] = create_maps_from_slice(input[41:81])

    # water to light
    almanac["water_to_light"] = create_maps_from_slice(input[83:99])

    # light to temperature
    almanac["light_to_temperature"] = create_maps_from_slice(input[101:141])

    # temperature to humidity
    almanac["temperature_to_humidity"] = create_maps_from_slice(input[143:181])

    # humidity to location
    almanac["humidity_to_location"] = create_maps_from_slice(input[183:219])

    return almanac


def part_one(input: List[str]) -> int:
    score = 0

    almanac = parse_almanac(input)

    return score


if __name__ == "__main__":
    score_one = part_one(read_input())

    print(score_one)
