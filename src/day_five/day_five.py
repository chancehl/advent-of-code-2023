import os
import functools

from typing import List, TypedDict, Tuple

# input.txt set
# SEED_TO_SOIL_START = 3
# SEED_TO_SOIL_END = 19

# SOIL_TO_FERTILIZER_START = 21
# SOIL_TO_FERTILIZER_END = 39

# FERTILIZER_TO_WATER_START = 41
# FERTILIZER_TO_WATER_END = 81

# WATER_TO_LIGHT_START = 83
# WATER_TO_LIGHT_END = 99

# LIGHT_TO_TEMPERATURE_START = 101
# LIGHT_TO_TEMPERATURE_END = 141

# TEMPERATURE_TO_HUMIDITY_START = 143
# TEMPERATURE_TO_HUMIDITY_END = 181

# HUMIDITY_TO_LOCATION_START = 183
# HUMIDITY_TO_LOCATION_END = 219

# input-b.txt set
SEED_TO_SOIL_START = 3
SEED_TO_SOIL_END = 5

SOIL_TO_FERTILIZER_START = 7
SOIL_TO_FERTILIZER_END = 10

FERTILIZER_TO_WATER_START = 12
FERTILIZER_TO_WATER_END = 16

WATER_TO_LIGHT_START = 18
WATER_TO_LIGHT_END = 20

LIGHT_TO_TEMPERATURE_START = 22
LIGHT_TO_TEMPERATURE_END = 25

TEMPERATURE_TO_HUMIDITY_START = 27
TEMPERATURE_TO_HUMIDITY_END = 29

HUMIDITY_TO_LOCATION_START = 31
HUMIDITY_TO_LOCATION_END = 33


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
    file_loc = os.path.join(os.path.dirname(__file__), "./input-b.txt")

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


def find_map(id: int, maps: List[FarmerMap]) -> FarmerMap:
    for map in maps:
        if (
            id >= map["source_range_start"]
            and id <= map["source_range_start"] + map["range_length"]
        ):
            return map

    return FarmerMap(desintation_range_start=id, source_range_start=id, range_length=0)


def compute_id(source_id: int, map: FarmerMap) -> int:
    return source_id + (map["desintation_range_start"] - map["source_range_start"])


def compute_location_number(seed: int, almanac: Almanac) -> int:
    # seed to soil
    soil_id = compute_id(seed, find_map(seed, almanac["seed_to_soil"]))

    # soil to fertilizer
    fertilizer_id = compute_id(
        soil_id, find_map(soil_id, almanac["soil_to_fertilizer"])
    )

    # fertilizer to water
    water_id = compute_id(
        fertilizer_id, find_map(fertilizer_id, almanac["fertilizer_to_water"])
    )

    # water to light
    light_id = compute_id(water_id, find_map(water_id, almanac["water_to_light"]))

    # light to temperature
    temperature_id = compute_id(
        light_id, find_map(light_id, almanac["light_to_temperature"])
    )

    # temperature to humidity
    humidity_id = compute_id(
        temperature_id, find_map(temperature_id, almanac["temperature_to_humidity"])
    )

    # humidity to location
    location_id = compute_id(
        humidity_id, find_map(humidity_id, almanac["humidity_to_location"])
    )

    print(
        f"CHAIN: {seed} -> {soil_id} -> {fertilizer_id} -> {water_id} -> {light_id} -> {temperature_id} -> {humidity_id} -> {location_id}"
    )

    return location_id


def parse_almanac(input: List[str]) -> Almanac:
    almanac = Almanac()

    # seed to soil
    almanac["seed_to_soil"] = create_maps_from_slice(
        input[SEED_TO_SOIL_START:SEED_TO_SOIL_END]
    )

    # soil to fertilizer
    almanac["soil_to_fertilizer"] = create_maps_from_slice(
        input[SOIL_TO_FERTILIZER_START:SOIL_TO_FERTILIZER_END]
    )

    # fertilizer to water
    almanac["fertilizer_to_water"] = create_maps_from_slice(
        input[FERTILIZER_TO_WATER_START:FERTILIZER_TO_WATER_END]
    )

    # water to light
    almanac["water_to_light"] = create_maps_from_slice(
        input[WATER_TO_LIGHT_START:WATER_TO_LIGHT_END]
    )

    # light to temperature
    almanac["light_to_temperature"] = create_maps_from_slice(
        input[LIGHT_TO_TEMPERATURE_START:LIGHT_TO_TEMPERATURE_END]
    )

    # temperature to humidity
    almanac["temperature_to_humidity"] = create_maps_from_slice(
        input[TEMPERATURE_TO_HUMIDITY_START:TEMPERATURE_TO_HUMIDITY_END]
    )

    # humidity to location
    almanac["humidity_to_location"] = create_maps_from_slice(
        input[HUMIDITY_TO_LOCATION_START:HUMIDITY_TO_LOCATION_END]
    )

    return almanac


def chunk(list, n: int):
    for i in range(0, len(list), n):
        yield list[i : i + n]


def parse_seed_numbers(input: List[str]) -> List[int]:
    raw_seed_number_line = input[0]
    raw_seed_number_line_parts = raw_seed_number_line.split("seeds: ")[1]
    raw_seed_numbers = raw_seed_number_line_parts.split(" ")

    return [int(seed_no) for seed_no in raw_seed_numbers]


def parse_seed_ranges(input: List[str]) -> List[Tuple[int, int]]:
    seed_ranges = []
    seed_numbers = parse_seed_numbers(input)

    if len(seed_numbers) % 2 != 0:
        raise Exception(
            "Could not parse seed ranges from input: Invalid number of seeds."
        )

    chunks = chunk(seed_numbers, 2)

    for start, length in chunks:
        seed_ranges.append((start, start + length))

    return seed_ranges


def part_one(input: List[str]) -> int:
    location_numbers = []

    almanac = parse_almanac(input)
    seeds = parse_seed_numbers(input)

    for seed in sorted(seeds):
        location_numbers.append(compute_location_number(seed, almanac))

    return min(location_numbers)


def part_two(input: List[str]) -> int:
    location_numbers = []

    almanac = parse_almanac(input)
    seeds = parse_seed_numbers(input)

    processed = 0
    maximum_seed = max(seeds)

    seed_ranges = parse_seed_ranges(input)

    for start, end in seed_ranges:
        if start == maximum_seed:
            maximum_seed = end

    for start, end in sorted(seed_ranges):
        for seed in range(start, end):
            processed += 1

            print(
                f"PROGRESS: processing seed #{processed} (id {seed}) ({round((seed/maximum_seed) * 100, 5)}%)"
            )

            location_numbers.append(compute_location_number(seed, almanac))

    return min(location_numbers)


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
