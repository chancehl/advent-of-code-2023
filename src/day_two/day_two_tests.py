import unittest

from .day_two import part_one, part_two


class DayOneTests(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(
            part_one(
                [
                    "15 blue, 6 red; 8 red; 1 green, 9 blue, 5 red",
                    "5 blue, 6 red; 8 red; 1 green, 9 blue, 5 red",
                ]
            ),
            2,
        )
        self.assertEqual(
            part_one(
                [
                    "5 blue, 6 red; 8 red; 1 green, 9 blue, 5 red",
                    "15 blue, 6 red; 8 red; 1 green, 9 blue, 5 red",
                    "10 blue, 6 red; 15 red; 1 green, 9 blue, 5 red",
                ]
            ),
            1,
        )

    def test_part_two(self):
        self.assertEqual(
            part_two(
                [
                    "1 blue, 1 red; 1 red; 1 green, 1 blue, 1 red",
                    "2 blue, 2 red; 2 red; 2 green, 2 blue, 2 red",
                ]
            ),
            9,
        )
