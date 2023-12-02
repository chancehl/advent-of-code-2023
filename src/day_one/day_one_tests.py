import unittest

from .day_one import part_one, part_two


class DayOneTests(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(part_one(["abc123"]), 13)
        self.assertEqual(part_one(["abc123", "abc1234"]), 27)
        self.assertEqual(part_one(["11", "11"]), 22)
        self.assertEqual(part_one(["akrer4ersr9e8r", "1asfirungnr2"]), 60)

    def test_part_two(self):
        self.assertEqual(part_two(["onetwothreefour"]), 14)
        self.assertEqual(part_two(["onetwothreefour", "fivesix"]), 70)
        self.assertEqual(part_two(["one89", "one"]), 30)
        self.assertEqual(part_two(["twoone8", "tasdfathree1"]), 59)
